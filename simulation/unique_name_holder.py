
class UniqueNameHolder:
    def __init__(self):
        self.__filenames = {}
        self.__flag_files_unque = True

    def set_names_unique_flag(self, flag):
        self.__flag_files_unque = flag

    def _purify_names(self, names):
        if not self.__flag_files_unque:
            return names[:]
        else:
            new_names = []
            for file_name in names:
                if self._check_name(file_name):
                    new_names.append(file_name)
            return new_names

    def _check_name(self, name):
        """returns True if name or part of name has NOT been recorded"""
        return all(name not in record for record in self.__filenames.values())

    def _add_unique_names(self, names_dict):
        self.__filenames.update(names_dict)

    def _remove_unique_name(self, key):
        self.__filenames.pop(key, None)

