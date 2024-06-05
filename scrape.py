#!/usr/bin/env python3

import argparse
import itertools
import json
import xmltodict
from xml.etree.ElementTree import fromstring, tostring

import requests

APPCAST_URL = 'https://desktop.docker.com/mac/main/{arch}/appcast.xml'
DOWNLOAD_URL = 'https://desktop.docker.com/mac/main/{arch}/{build}/Docker.dmg'
SPARKLE_NS = '{http://www.andymatuschak.org/xml-namespaces/sparkle}'

def get_latest_build_number(arch):
    """
    Parse the appcast XML to find the Build number of the latest release.
    """
    arch_url = APPCAST_URL.format(arch=arch)
    print('\nURL = {}\n'.format(arch_url))
    resp = requests.get(arch_url)
    print('\nResponse Text = \n{}\n'.format(resp.text))

    ns = {'sparkle': SPARKLE_NS}
    print('\nns = {}\n'.format(ns))

    root = fromstring(resp.text)
    root_attrib = root.attrib
    print('\nRoot Attrib = {}\n'.format(root_attrib))
    root_keys = root.keys()
    print('\nRoot Keys = {}\n'.format(root_keys))
    root_items = root.items()
    print('\nRoot Items = {}\n'.format(root_items))

    enclosures = root.findall('.//enclosure', ns)
    enclosures_length = 0 or len(enclosures)
    print('\nEnclosures Length = {}\n'.format(enclosures_length))

    for (idx, enclosure) in enumerate(enclosures):
        print('\nEnclosure Keys = {}\n'.format(enclosure.keys()))
        print('\nEnclosure Items = {}\n'.format(enclosure.items()))
        print('\nEnclosure JSON = {}\n'.format(xmltodict.parse(tostring(enclosure))))

        url_attrib = 'url'.format(ns=ns['sparkle'])
        print('\nEnclosure URL Attribute: {}\n'.format(url_attrib))
        url = enclosure.attrib[url_attrib]
        print('\nEnclosure URL: {}\n'.format(url))

        previous_build_attrib = 'previousBuild'.format(ns=ns['sparkle'])
        print('\nEnclosure Prev Build Attribute: {}\n'.format(previous_build_attrib))
        previous_build = enclosure.attrib[previous_build_attrib]
        print('\nEnclosure Previous Build: {}\n'.format(previous_build))

        version_attrib = '{}version'.format(SPARKLE_NS, ns=ns['sparkle'])
        print('\nEnclosure Version Attribute: {}\n'.format(version_attrib))
        version = enclosure.attrib[version_attrib]
        print('\nEnclosure Version: {}\n'.format(version))

        return int(version)
    return None


def scan(arch, latest_build, limit=None):
    build_limit = latest_build - limit if limit else 0

    builds = []
    for build in range(latest_build, build_limit, -1):
        try:
            resp = requests.head(DOWNLOAD_URL.format(
                arch=arch,
                build=build
            ))
            resp.raise_for_status()
        except requests.exceptions.RequestException:
            continue

        headers = resp.headers
        print('\nArch = {}\n\nBuild = {}\n\nHeaders = {}\n'.format(arch, build, headers))

        headers['url'] = resp.url
        builds.append(dict(headers))

    return builds


def main():
    parser = argparse.ArgumentParser(
        description='Scrape for Docker for Mac release download links'
    )
    parser.add_argument('arch', choices=['amd64', 'arm64'])
    parser.add_argument('--limit', type=int,
                        help='Maximum number of builds to scan for')
    parser.add_argument('--out', type=str,
                        help='JSON file to output build info')
    args = parser.parse_args()
    print('Args = {}.'.format(args))

    if args.out is None:
        args.out = args.arch + '.json'

    latest_build = get_latest_build_number(args.arch)
    print('\nLatest Build = {}\n'.format(latest_build))

    builds = scan(args.arch, latest_build, limit=args.limit)
    print('\nBuilds = {}\n'.format(builds))

    with open(args.out, 'w') as f:
        json.dump(builds, f)

    print('\nWrote {}\n'.format(args.out))


if __name__ == '__main__':
    main()

