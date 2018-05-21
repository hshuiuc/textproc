# Indexer.py

from avl_tree import AVLTreeMap
from unsorted_table_map import UnsortedTableMap
from sorted_table_map import SortedTableMap
from chain_hash_map import ChainHashMap
from probe_hash_map import ProbeHashMap
from splay_tree import SplayTreeMap
from red_black_tree import RedBlackTreeMap
from collections import OrderedDict

from time import time


class Indexer:
    """A class for indexing preprocessed text documents."""
    __structures = {'avl': AVLTreeMap(), 'unsorted': UnsortedTableMap(),
                    'sorted': SortedTableMap(), 'chain': ChainHashMap(),
                    'probe': ProbeHashMap(), 'splay': SplayTreeMap(),
                    'rb': RedBlackTreeMap(), 'dict': dict(),
                    'od': OrderedDict()}
    __names = {'avl': 'AVL Tree Map', 'unsorted': 'Unsorted Table Map',
               'sorted': 'Sorted Table Map', 'chain': 'Chain Hash Map',
               'probe': 'Probe Hash Map', 'splay': 'Splay Tree Map',
               'rb': 'Red and Black Tree Map', 'dict': 'Python Dictionary',
               'od': 'Python Ordered Dictionary'}

    def __init__(self, original, preprocessed, indexed=None, map_type='rb'):
        self.__pre_file = open(preprocessed, 'r', encoding='utf-8-sig')
        self.__org_file = open(original, 'r', encoding='utf-8-sig')
        self.__map_type = map_type
        self._mapFix(self.__map_type)
        self.__multimap = self.__structures[self.__map_type]
        self.__average = 0
        self.__median = 0
        self.__indexing_time = 0
        self.__index_out = indexed

    def _mapFix(self, map_type):
        if map_type not in self.__structures:
            self.__map_type = 'avl'

    def index(self):
        """ reads the preprocessed file and indexes the words."""
        initial_time = time()
        total_terms = 0
        for i, line in enumerate(self.__pre_file):
            line_num = i + 1
            for word in line.strip().split():
                try:
                    self.__multimap[word].append(line_num)
                    total_terms += 1
                except:
                    self.__multimap[word] = [line_num]
                    total_terms += 1
        self.__indexing_time = time() - initial_time
        print('Indexing duration is {} seconds.'.format(
            round(self.__indexing_time, 4)))
        self.__average = total_terms / len(self.__multimap)
        self._find_median()

    def dump(self):
        """Writes the index list to a file"""
        if self.__index_out is not None:
            out_file = open(self.__index_out, 'w')
            for word in self.__multimap:
                lines = str(self.__multimap[word])[1:-1]
                output = '{} {}\n'.format(word, lines)
                out_file.write(word + ' ' + lines + '\n')
            out_file.close()

    def _find_median(self):
        frequencies = list()
        for key in self.__multimap:
            frequencies.append(len(self.__multimap[key]))
        frequencies.sort()
        self.__median = frequencies[len(frequencies) // 2]

    def _search(self, keyword):
        initial_time = time()
        lines = self.__multimap[keyword]
        search_time = time() - initial_time
        keyword = keyword
        for i, text in enumerate(self.__org_file):
            line_num = i + 1
            if line_num in lines:
                print('{1}: {0}'.format(text.strip(), line_num))
        self.__org_file.seek(0)  # resets buffer for next searches
        print('\nIt took {:.12f} seconds to find {} occurrence '
              'of {!r}.'.format(search_time, len(lines), keyword))

    def startUI(self):
        """Runs a loop and for a word. Return occurrence and lines
         it appeared on"""
        print('This search is powered by {}.'.format(
            self.__names[self.__map_type]))
        while True:
            try:
                keyword = input('Enter a word to search for: ').lower()
                if len(keyword) < 3 or not keyword.isalpha():
                    raise ValueError()
                self._search(keyword)
            except KeyError:
                print("Sorry! We couldn't find {!r} in "
                      "the file.\n".format(keyword))
            except RecursionError:
                print("Structure recursion limit has exceeded, please try"
                      " another map!")
            except ValueError:
                print('Invalid Term!\n\tOnly alphabetical words with three or'
                      ' more characters are allowed!')
            except:
                print('Error has been occurred!')
            if input("Quit? (y/n): ").lower().startswith('y'):
                break

    def __repr__(self):
        """prints the stats table."""
        output = 'Total indexed terms:\t{}\n'.format(len(self.__multimap))
        output += 'Average word frequency:\t{}\n'.format(
            round(self.__average, 2))
        output += 'Median word frequency:\t{}\n'.format(self.__median)
        return output


if __name__ == '__main__':
    print('Indexer is a text indexing class.')
