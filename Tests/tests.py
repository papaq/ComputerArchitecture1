__author__ = 'solomon'

import unittest
from Python.main import *
from time import gmtime, strftime


class TestFuncs(unittest.TestCase):
    def test_a_make_cities_counter_list(self):
        counter = [0, 0, 0]
        _len = 3
        self.assertEqual(make_cities_counter_list(_len), counter)

    def test_b_find_all_mentions(self):
        news_line = "lviv Lvova lvovu"
        city = 'lviv'
        self.assertEqual(find_all_mentions(news_line, city), 1)

    def test_c_count_all_cities(self):
        news_line = "lviv Lvova lvovu"
        vocabulary_set = [['lviv'], ['lvova'], ['lvovu']]
        counter = [3]
        self.assertEqual(count_all_cities(news_line, vocabulary_set, counter), [5])

    def test_d_sort_list(self):
        mention_list = [1, 4, 3, 1]
        vocabulary = ['kyiv', 'odesa', 'lviv', 'luhansk']
        sorted_line = [(1, 'kyiv'), (1, 'luhansk'), (3, 'lviv'), (4, 'odesa')]
        self.assertEqual(sort_list(mention_list, vocabulary), sorted_line)

    def test_e_list_all_lines(self):
        file_name = '/home/solomon/PycharmProjects/Lab1/Tests/test_list_lines.txt'
        result_list = ['line1\n', 'line2\n', 'line3\n']
        self.assertEqual(list_all_lines(file_name), result_list)

    def test_f_make_cities_vocabulary(self):
        file_name = '/home/solomon/PycharmProjects/Lab1/Tests/test_list_lines.txt'
        result_list = [['line1\n', 'line2\n', 'line3\n']]
        self.assertEqual(make_cities_vocabulary([file_name]), result_list)

    def test_g_make_channel_list(self):
        file_name = '/home/solomon/PycharmProjects/Lab1/Tests/test_channel_list_func.xml'
        result_list = ['http://www.pravda.com.ua/rss/view_news/']
        self.assertEqual(make_channel_list(file_name), result_list)

    def test_h_get_item(self):
        class RSS:
            entries = ["e1", "e2"]

            def __init__(self):
                pass

        self.assertEqual(get_item(RSS), ["e1", "e2"])

#    @patch('get_item')
    def test_i_run_all_rss(self):
        class Item:
            published_parsed = strftime("%Y %b %d %H %M %S", gmtime())
            title = "title"

            def __init__(self):
                pass

        class RSS:
            entries = [Item, Item]

            def __init__(self):
                pass

        all_rss = ["this is rss channel #1"]
        vocabulary_list = [['city1', 'city2']]
        self.assertEqual(run_all_rss(all_rss, vocabulary_list), [0, 0])


if __name__ == "__main__":
    unittest.main()
