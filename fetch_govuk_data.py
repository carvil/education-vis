import os
import csv
import sys
import ipdb
import json
import time
import argparse
import requests
import requests_cache
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup
from requests_cache import CachedSession
from requests.adapters import HTTPAdapter


session = CachedSession(cache_name='govuk_cache', backend='sqlite')
session.mount('http://', HTTPAdapter())
session.mount('https://', HTTPAdapter())


def test_base_path(original_url):
    """
    Given a URL, perform a HEAD request and fetch the actual URL (in case there
    are redirects) and return that.
    """
    response = session.head(original_url, allow_redirects=True)

    if 200 <= response.status_code < 300:
        return response.url
    elif response.status_code == 429:
        response.raise_for_status()
    else:
        if response.status_code not in (410,):
            sys.stderr.write("Unexpected response {} for {}\n".format(response.status_code, original_url))
        return None


def fetch_education_urls(input_file):
    """
    Given a local input file, parse it and return a list of GOV.UK URLs.
    """
    documents = []
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        # skip headers
        next(reader, None)
        documents = list(reader)

    return [document[0] for document in documents]


def fetch_metadata(url):
    """
    Given a GOV.UK URL, this function fetches the page from the content store
    and extracts the information about where it's published/rendered and also
    the various data formats.
    """
    govuk_url = test_base_path(url)

    content_store_url = govuk_url.replace(
        "https://www.gov.uk/",
        "https://www.gov.uk/api/content/"
    )

    r = session.get(content_store_url, verify=False, timeout=10)
    json_data = r.json()
    links = json_data.get('links')
    taxons = links.get('taxons')
    taxon_title = ''
    taxon_base_path = ''
    taxon_description = ''

    if taxons and len(taxons) > 0:
        taxon = taxons[0]
        taxon_title = taxon.get(u'title')
        taxon_base_path = taxon.get(u'base_path')
        taxon_description = taxon.get(u'description')

    return [
        json_data.get('content_id'),
        json_data.get('rendering_app') or '',
        json_data.get('publishing_app'),
        json_data.get('document_type'),
        json_data.get('format'),
        json_data.get('schema_name'),
        taxon_title,
        taxon_base_path,
        taxon_description
    ]


if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    requests_cache.install_cache()

    csvfile = open(output_file, 'wb')
    content_writer = csv.writer(csvfile, delimiter=',')
    content_writer.writerow(
        ['URL', 'content_id', 'rendering_app', 'publishing_app', 'document_type', 'format', 'schema_name']
    )
    urls = fetch_education_urls(input_file)

    for idx, url in enumerate(urls):
        try:
            print("===> Processing URL #" + str(idx) + " - " + url)
            data = fetch_metadata(url)
            content_writer.writerow([url] + data)
        except:
            content_writer.writerow([url, ''])
