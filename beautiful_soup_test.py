#! /usr/bin/env python3

import json
import pandas as pd
import httplib2
from bs4 import BeautifulSoup, SoupStrainer

def find_link():
    http = httplib2.Http()
    sources_list = []
    status, response = http.request('https://distfiles.gentoo.org/releases/amd64/autobuilds/current-stage3-amd64-hardened-selinux-openrc/')
    for link in BeautifulSoup(response, parse_only=SoupStrainer('a'), features="xml").find_all('a', href=True):
        print(link['href'])
        sources_list.append(link['href'])
    df = pd.DataFrame(sources_list)
    return df

sources_ = find_link()

        