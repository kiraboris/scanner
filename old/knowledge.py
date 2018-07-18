# python 2,3
#
# Functions for User <-> Knowledge interaction
#

import easygui as gui
from importlib.machinery import SourceFileLoader

# alias
first = next


class SourceDB:

    def __init__(self, filename, flag_autosave=True):

        modulename = filename.split('/')[-1].split('.')[0]
        self.__db = SourceFileLoader(modulename, filename).load_module()
        self.__filename = filename
        self.__autosave = flag_autosave
        self.__observed_names = set()

    def save(self):

        self.__savebuf(self.__update_blocks(self.__loadbuf()))

    def __loadbuf(self):

        with open(self.__filename, 'r') as me:
            buf = me.readlines()

        return buf

    def __savebuf(self, buf):

        with open(self.__filename, 'w') as me:
            me.writelines(buf)

    def __update_blocks(self, buf):

        for name in self.__observed_names:
            buf = self.__update_block(buf, name)

        return buf

    def __update_block(self, buf, name):

        start_i, end_i = self.__find_block(buf, name)

        return buf[:start_i] + [self.__make_block(name)] + buf[end_i + 1:]

    def __make_block(self, name):

        title = name + ' = '

        replacement = ',\n' + ' ' * len(title)

        return title + repr(self.__get(name)).replace(',', replacement) + '\n'

    def __find_block(self, buf, name):

        try:
            start_i = first(i for (i, line) in enumerate(buf) if name in line)
        except StopIteration:
            start_i = 0

        end_i = first(i for (i, _) in enumerate(buf[start_i:])
                      if self.__is_matched(buf[start_i:i+1]))

        return start_i, end_i

    @staticmethod
    def __is_matched(lines):

        expression = "\n".join(lines)

        opening = '({['
        closing = ')}]'
        mapping = dict(zip(opening, closing))

        stack = []
        for letter in expression:
            if letter in opening:
                stack.append(mapping[letter])
            elif letter in closing:
                if not stack or letter != stack.pop():
                    return False

        return not stack

    def __get(self, key):

        return vars(self.__db)[key]

    def __getattr__(self, key):

        self.__observed_names.add(key)

        return self.__get(key)


def ask(text="", **kwargs):
    """
        may be custom input method
    """

    result = input(text, **kwargs)

    return result


def say(text="", **kwargs):
    """
        may be custom output method
    """

    print(text, kwargs)


def ask_filename(**kwargs):

    return gui.fileopenbox(kwargs)
