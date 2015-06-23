__author__ = 'solomon'

import feedparser
import xml.etree.cElementTree as eT
import time
import ConfigParser
from main_gevent import *


def list_all_lines(file_name):
    return [line for line in open(file_name)]


def make_cities_vocabulary(vocabulary_list):
    return [list_all_lines(name) for name in vocabulary_list]


def make_channel_list(file_name):
    return [item.text.translate(None, '\n ')
            for item in eT.parse(open(file_name)).getroot().iter('url')]


def get_rss(url):
    return feedparser.parse(url)


def make_cities_counter_list(_len):
    return [0 * i for i in xrange(_len)]


def get_item(rss):
    return [item for item in rss.entries]


# def get_fulltext(rss):
#    return [item.fulltext for item in rss.entries]


def find_all_mentions(news_line, city):
    return news_line.count(city.translate(None, '\n '))


def count_all_cities(news_line, vocabulary_set, counter_line):
    # counter_line = _counter_line
    for city in xrange(len(counter_line)):
        for vocabulary in vocabulary_set:
            counter_line[city] += \
                find_all_mentions(news_line, vocabulary[city])
    return counter_line


def run_all_rss(all_rss, vocabulary_set):
    counter_line = make_cities_counter_list(len(vocabulary_set[0]))
    for channel in all_rss:
        for item in get_item(get_rss(channel)):
            if item.published_parsed[0] * 365.25 \
                    + item.published_parsed[1] * 30.5 \
                    + item.published_parsed[2] \
                    + float(item.published_parsed[3]) / 24 > days_gone - 1:
                counter_line = count_all_cities(
                    item.title.encode("utf-8"), vocabulary_set, counter_line)
    return counter_line


def sort_list(mention_list, vocabulary):
    statistics = []
    for city in xrange(len(vocabulary)):
        statistics.append((mention_list[city], vocabulary[city]))
    return sorted(statistics, key=lambda city_mentioned: city_mentioned[0], )


def make_result_xml(result, file_name):
    root = eT.Element('data')
    cities_branch = eT.SubElement(root, 'items')

    for cities in result:
        city = eT.SubElement(cities_branch, 'city')
        eT.SubElement(city, 'name').text = cities[1].translate(
            None, '\n ').decode('utf-8')
        eT.SubElement(city, 'mentions').text = str(cities[0])

    tree = eT.ElementTree(root)
    tree.write(file_name, 'utf-8')


def print_top_10(sorted_list):
    for city in xrange(len(sorted_list) - 1,
                       len(sorted_mention_list) - 11, -1):
        print("\n".join(["%s : %d" % (
            sorted_list[city][1].translate(None, '\n'),
            sorted_list[city][0])]))

if __name__ == '__main__':

    config = ConfigParser.RawConfigParser()
    config.read('../h.config')
    mode = config.get('way', 'mode')

    start_time = time.time()

    vocabularies = make_cities_vocabulary([
        'cities.txt',
        'cities_2.txt',
        'cities_3.txt',
        'cities_5.txt',
        'cities_adj.txt'])

    days_gone = float(time.strftime("%Y")) * 365.25 + float(
        time.strftime("%m")) * 30.5 + float(
        time.strftime("%d")) + float(time.strftime("%H")) / 24

    if mode == "gevent":
        print ('Searching started in %s mode' % mode)
        mentions = run_all_rss_gevent(make_channel_list('channels.xml'), vocabularies, days_gone)
    elif mode == "simple":
        print ('Searching started in %s mode' % mode)
        mentions = run_all_rss(make_channel_list('channels.xml'), vocabularies)
    else:
        print('Mode is inappropriate!')
        exit()

    print('\nSearching lasted %s seconds' % (time.time() - start_time))

    sorted_mention_list = sort_list(mentions, vocabularies[0])

    print_top_10(sorted_mention_list)

    make_result_xml(sorted_mention_list, "rusalochka.xml")
