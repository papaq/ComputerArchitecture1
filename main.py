__author__ = 'solomon'

import feedparser
import xml.etree.cElementTree as eT
import time


def list_all_lines(file_name):
    return [line for line in open(file_name)]


def make_cities_vocabulary():
    voc1 = list_all_lines('cities.txt')
    voc2 = list_all_lines('cities_2.txt')
    voc3 = list_all_lines('cities_3.txt')
    voc4 = list_all_lines('cities_5.txt')
    voc_adj = list_all_lines('cities_adj.txt')
    return [voc1, voc2, voc3, voc4, voc_adj]


def make_channel_list(file_name):
    return [item.text.translate(None, '\n ') for item in eT.parse(open(file_name)).getroot().iter('url')]


def get_rss(url):
    return feedparser.parse(url)


def make_cities_counter_list(_len):
    return [0 * i for i in range(0, _len)]


def get_item(rss):
    return [item for item in rss.entries]


def get_fulltext(rss):
    return [item.fulltext for item in rss.entries]


def find_all_mentions(news_line, city):
    return news_line.count(city.translate(None, '\n '))


def count_all_cities(news_line, vocabulary_set, counter_line):
    # counter_line = _counter_line
    for city in xrange(len(counter_line)):
        for vocabulary in vocabulary_set:
            counter_line[city] += find_all_mentions(news_line, vocabulary[city])
    return counter_line


def run_all_rss(all_rss, vocabulary_set):
    counter_line = make_cities_counter_list(len(vocabulary_set[0]))
    for channel in all_rss:
        for item in get_item(get_rss(channel)):
            if item.published_parsed[0]*365.25 + item.published_parsed[1]*30.5 + item.published_parsed[2] > days_gone-1:
                counter_line = count_all_cities(item.title.encode("utf-8"), vocabulary_set, counter_line)
    return counter_line


def sort_list(mention_list, vocabulary):
    statistics = []
    for city in xrange(len(vocabulary)):
        statistics.append((mention_list[city], vocabulary[city]))
    return sorted(statistics, key=lambda city_mentioned: city_mentioned[0], )


def print_top_10(sorted_list):
    for city in xrange(len(sorted_list) - 1, len(sorted_mention_list) - 11, -1):
        print("\n".join(["%s : %d" % (sorted_list[city][1].translate(None, '\n'), sorted_list[city][0])]))


vocabularies = make_cities_vocabulary()
now = time.strftime("%D").split("/")
days_gone = float(time.strftime("%Y"))*365.25 + float(time.strftime("%m"))*30.5 + float(time.strftime("%d"))

# print(make_channel_list('channels.xml'))
# print(list_all_lines('cities.txt')[1])

# channels = get_rss(make_channel_list('channels.xml')[3])
# print(channels.entries[9].title)
# print(channels)
# print()

# print(make_cities_counter_list(5))
# print(get_fulltext(get_rss(make_channel_list('channels.xml')[3]))[0])

# print(find_all_mentions("abca b cabc a", "ca"))
# print(count_all_cities("lviv Lvova lvovu", [['lviv'], ['lvova'], ['lvovu']], [1]))

# print(count_all_cities(channels.entries[9].title.encode("utf-8"),
#       make_cities_vocabulary(),
#       make_cities_counter_list(101)))

mentions = run_all_rss(make_channel_list('channels.xml'), vocabularies)

# print(mentions)

# print(get_fulltext(get_rss(make_channel_list('channels.xml')[4]))[0])
# print(get_title(get_rss(make_channel_list('channels.xml')[4]))[0])
# print(get_rss(make_channel_list('channels.xml')[0]))

sorted_mention_list = sort_list(mentions, vocabularies[0])

print_top_10(sorted_mention_list)
