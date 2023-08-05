#!/usr/bin/env python3
from asyncio import get_event_loop, gather, Semaphore
from collections import defaultdict
from datetime import datetime
from json import dumps
from logging import getLogger, basicConfig, INFO
from os import environ, cpu_count
from pathlib import Path
from random import choice
from sys import path
from warnings import filterwarnings

import requests
from mergedeep import merge
from requests import RequestException
from urllib3.exceptions import InsecureRequestWarning
from yaml import safe_load as load

if not __package__:
    path.insert(0, str(Path(Path(__file__).parent.parent.parent)))

from cloudrecon import __version__
from cloudrecon.constants import useragent_list, aws_format_list, gcp_format_list, azure_format_list, alibaba_format_list
from cloudrecon.mongodb import MongoDB, Hit, Access

filterwarnings("ignore", category=InsecureRequestWarning)
cpus = cpu_count() or 1

logger = getLogger(__name__)

# TODO: opt to change log-level
basicConfig(format="%(message)s", level=INFO)


def bucket_exists(url, timeout):
    exists = False
    public = False

    try:
        res = requests.head(
            url,
            headers={"User-Agent": choice(useragent_list)},
            verify=False,
            timeout=timeout,
        )
        # TODO: handle redirects
        status_code = res.status_code
        exists = status_code != 404
        public = status_code == 200
    except RequestException:
        pass

    return exists, public


async def find_bucket(url, timeout, db, sem):
    async with sem:
        exists, public = bucket_exists(url, timeout)

        if exists:
            access = Access.PUBLIC if public else Access.PRIVATE
            access_key = repr(access)
            access_word = str(access).upper()
            logger.info(f"{access_key} {access_word} {url}")

            hit = Hit(url, access)
            if db and hit.is_valid():
                db.update({"url": url}, dict(hit))
            return Hit(url, access)

        return None


def collect_results(hits):
    d = defaultdict(list)
    for hit in hits:
        url = hit.url
        access = repr(hit.access)
        d[access].append(url)

    return d.get(repr(Access.PRIVATE), []), d.get(repr(Access.PUBLIC), [])


def read_config():
    config = {}

    config_hierarchy = [
        Path(Path(__file__).parent, "cloudrecon.yml"),  # default
        Path(Path.home(), "cloudrecon.yaml"),
        Path(Path.home(), "cloudrecon.yml"),
        Path(Path.cwd(), "cloudrecon.yaml"),
        Path(Path.cwd(), "cloudrecon.yml"),
        Path(environ.get("cloudrecon_CONFIG") or ""),
    ]

    for c in config_hierarchy:
        try:
            c = load(open(c, "r")) or {}
            merge(config, c)
        except (IOError, TypeError):
            pass

    return config


def json_output_template(key, total, hits, exclude):
    return {} if exclude else {key: {"total": total, "hits": hits}}


def main(words, timeout, concurrency, output, use_db, only_public, cloudtype):
    start = datetime.now()
    loop = get_event_loop()

    config = read_config()
    database = config.get("database")
    separators = config.get("separators") or [""]
    environments = config.get("environments") or [""]

    ## This is where I will make the switch between AWS, GCP, Azure, and Alibaba
    if cloudtype == 'AWS':
        awsregions = config.get("aws-regions") or [""]
        url_list = {
            f.format(
                awsregion=f"{awsregion}",
                word=word,
                sep=sep,
                env=env,
            )
            for f in aws_format_list
            for awsregion in awsregions
            for word in words
            for sep in separators
            for env in environments
        }
    elif cloudtype == 'GCP':
        url_list = {
            f.format(
                word=word,
                sep=sep,
                env=env,
            )
            for f in gcp_format_list
            for word in words
            for sep in separators
            for env in environments
        }

    elif cloudtype == 'Azure':
        url_list = {
            f.format(
                word=word,
                env=env,
            )
            for f in azure_format_list
            for word in words
            for env in environments
        }

    elif cloudtype == 'Alibaba':
        aliregions = config.get("alibaba-regions") or [""]
        url_list = {
            f.format(
                aliregion=f"{aliregion}",
                word=word,
                sep=sep,
                env=env,
            )
            for f in alibaba_format_list
            for aliregion in aliregions
            for word in words
            for sep in separators
            for env in environments
        }

    elif cloudtype is None:
        print("Cloudtype not presented, please input one of the following: AWS, GCP, Azure, or Alibaba")

    db = MongoDB(host=database["host"], port=database["port"]) if use_db else None
    sem = Semaphore(concurrency)

    tasks = gather(
        *[
            find_bucket(
                url,
                timeout,
                db,
                sem
            )
            for url in url_list
        ]
    )
    hits = filter(bool, loop.run_until_complete(tasks))

    private, public = collect_results(hits)

    if output:
        json_result = {
            **json_output_template(
                str(Access.PRIVATE), len(private), private, only_public
            ),
            **json_output_template(str(Access.PUBLIC), len(public), public, False),
        }

        output.write(dumps(json_result, indent=4))
        logger.info(f"Output written to file: {output.name}")

    stop = datetime.now()
    logger.info(f"Complete after: {stop - start}")


def cli():
    import argparse

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=lambda prog: argparse.HelpFormatter(
            prog, max_help_position=35, width=100
        ),
    )
    parser.add_argument(
        "-o",
        "--output",
        type=argparse.FileType("w"),
        metavar="file",
        help="Write output to <file>",
    )
    parser.add_argument(
        "-d",
        "--db",
        action="store_true",
        help="Write output to database"
    )
    parser.add_argument(
        "-p",
        "--public",
        action="store_true",
        help="Only include 'public' buckets in the output",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        metavar="seconds",
        default=30,
        help="HTTP request timeout in <seconds> (default: 30)",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "-c",
        "--concurrency",
        type=int,
        metavar="num",
        default=cpus,
        help=f"Maximum <num> of concurrent requests (default: {cpus})",
    )
    parser.add_argument(
        '-ct',
        '--cloudtype',
        action='store',
        dest='cloudtype',
        help='Input which cloud platform to query: "AWS", "GCP", "Azure", or "Alibaba"'
        )
    parser.add_argument(
        "word_list",
        nargs="+",
        type=argparse.FileType("r"),
        help="Read words from one or more <word-list> files",
    )
    args = parser.parse_args()

    output = args.output
    db = args.db
    timeout = args.timeout
    concurrency = args.concurrency
    public = args.public
    words = {l.strip() for f in args.word_list for l in f}
    cloudtype = args.cloudtype

    main(words=words, timeout=timeout, concurrency=max(1, concurrency), output=output, use_db=db, only_public=public, cloudtype=cloudtype)


if __name__ == "__main__":
    cli()
