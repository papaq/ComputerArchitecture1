__author__ = 'solomon'
# -*- coding: cp1251 -*-

import feedparser
import xml.etree.cElementTree as eT


def list_all_lines(file_name):
    return [line for line in open(file_name)]


def make_channel_list(file_name):
    return [item.text.translate(None, '\n ') for item in eT.parse(open(file_name)).getroot().iter('url')]


def get_rss(url):
    return feedparser.parse(url)


def make_cities_counter_list(_len):
    return [0 * i for i in range(0, _len)]


def rss_watch(rss):
    l = []
    for item in rss.entries:
        l.append(item.title + '\n')
    return l


print(make_channel_list('channels.xml'))
print(list_all_lines('cities.txt')[1])
print(get_rss(make_channel_list('channels.xml')[3]))
print(make_cities_counter_list(5))
print(rss_watch(get_rss(make_channel_list('channels.xml')[3])))
