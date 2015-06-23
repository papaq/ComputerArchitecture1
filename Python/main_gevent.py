__author__ = 'solomon'

import gevent
from Python.main import *


def run_all_rss_gevent(all_rss, vocabulary_set, days_gone):
    counter_line = make_cities_counter_list(len(vocabulary_set[0]))
    work = [gevent.spawn(look_through_channel_gevent, channel, vocabulary_set, counter_line, days_gone) for channel in all_rss]
    gevent.joinall(work)

    return counter_line


def look_through_channel_gevent(channel, vocabulary_set, counter_line, days_gone):
    for item in get_item(get_rss(channel)):
            if item.published_parsed[0] * 365.25 \
                    + item.published_parsed[1] * 30.5 \
                    + item.published_parsed[2] \
                    + float(item.published_parsed[3]) / 24 > days_gone - 1:
                counter_line = count_all_cities(
                    item.title.encode("utf-8"), vocabulary_set, counter_line)
    return counter_line
