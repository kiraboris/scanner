
from ..entities.quanta import qdict


def correct(corrector, entries, file_format):
    """Backbone to correct wrong splits or blends
       Delegate 'corrector' may not be None and implements:
        * find_mergable_with_state(states, state)
        * find_mergable_with_line(lines, line)
        * merge_lines(blends)
        * merge_states(blends)
        * split_line(lines, line, flag_require_all_spilts)
        * split_state(states, state)
    """

    # make O(1) lookup dict
    dict_entries = qdict(entries)

    # merge blends (assumption: entries partitioned into mergable classes)
    result = []
    ignore = set()
    for cur in entries:

        if cur.qid in ignore:
            continue

        blends = __find_mergable(dict_entries, cur, file_format, corrector)

        if len(blends) > 1:
            result.append(__merge(blends, file_format, corrector))
            ignore.update([x.qid for x in blends])
        else:
            result.append(cur)
            ignore.add(cur.qid)

    # make splits
    result2 = []
    for cur in result:
        splits = __split(dict_entries, cur, file_format, corrector)

        result2.extend(splits)

        dict_entries.update(qdict(splits))

    return result2


def make_mrg(cat_lst, lin_lst):
    """Look for cat entries in lin and merge the two files into mrg"""
    result = []

    lin_dict = qdict(lin_lst)

    for entry_cat in cat_lst:
        entry_mrg = entry_cat.copy()

        if entry_mrg.qid in lin_dict:
            entry_lin = lin_dict[entry_mrg.qid]

            entry_mrg.freq = entry_lin.freq
            entry_mrg.freq_err = entry_lin.freq_err
            entry_mrg.int_cat_tag = -abs(entry_mrg.int_cat_tag)

        result.append(entry_mrg)

    return result


def __find_mergable(self, dict_entries, cur, file_format, corrector):

    if 'cat' in file_format or 'lin' in file_format:
        return self.__corrector.find_mergable_with_line(dict_entries, cur)
    elif 'egy' in file_format:
        return self.__corrector.find_mergable_with_state(dict_entries, cur)
    else:
        raise Exception('File format unknown')


def __merge(self, blends, file_format, corrector):

    if 'cat' in file_format or 'lin' in file_format:
        return self.__corrector.merge_lines(blends)
    elif 'egy' in file_format:
        return self.__corrector.merge_states(blends)
    else:
        raise Exception('File format unknown')


def __split(self, dict_entries, cur, file_format, corrector):

    if 'cat' in file_format:
        return self.__corrector.split_line(dict_entries, cur, flag_require_all_spilts=True)
    elif 'lin' in file_format:
        return self.__corrector.split_line(dict_entries, cur, flag_require_all_spilts=False)
    elif 'egy' in file_format:
        return self.__corrector.split_state(dict_entries, cur)
    else:
        raise Exception('File format unknown')