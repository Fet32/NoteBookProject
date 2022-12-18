import os
import pickle
import platform


class Contacts:

    def __init__(self, dict_contact):
        for key, value in dict_contact.items():
            setattr(self, key, value)

    def get_uid(self, key_fields):
        return '_'.join([getattr(self, value) for value in key_fields])

    def get_fields(self):
        return self.__dict__.keys()


class NoteBook:
    # if platform.system() == 'Windows':
    #     noteBookDir = os.path.join(os.getenv('HOMEDRIVE'), os.getenv('HOMEPATH'))
    # else:
    #     noteBookDir = os.getenv('HOME')
    noteBookDir = os.getcwd() + os.sep + 'notebook'

    @classmethod
    def get_books_dir(cls):
        return cls.noteBookDir

    @classmethod
    def set_books_dir(cls, note_book_dir):
        cls.noteBookDir = note_book_dir

    @classmethod
    def get_usernames(cls):
        if not os.path.exists(cls.noteBookDir):
            return []
        else:
            return [item for item in os.listdir(cls.noteBookDir) if os.path.isdir(os.path.join(cls.noteBookDir, item))]

    @classmethod
    def get_books_names(cls, username):
        if not username:
            return []
        path_dir = cls.noteBookDir + os.sep + username
        if not os.path.exists(path_dir):
            return []
        else:
            return [os.path.splitext(item)[0] for item in os.listdir(path_dir) if
                    os.path.isfile(os.path.join(path_dir, item)) and os.path.splitext(item)[1] == '.data']

    @staticmethod
    def print_contact_list(contact_list):
        count = 1
        for item in contact_list:
            print(count, end='.')
            print(', '.join([value for value in item.values()]))
            count += 1

    # def get_books_dir(self):
    #     return self.noteBookDir

    def __init__(self, user, book_name):
        self.user = user
        self.book_name = book_name
        self.info = ''
        self.__set_dir()
        self.work_file = self.__set_work_file()
        self.cfg_file = self.__set_work_file('cfg')
        self.stored_data = self.__read_file()
        self.stored_config = self.__read_file('cfg_file')

    def __set_work_file(self, file_extension='data'):
        work_file = os.path.join(self.noteBookDir, self.book_name + '.' + file_extension)
        return work_file

    def __set_dir(self):
        self.noteBookDir += os.sep + self.user
        if not os.path.exists(self.noteBookDir):
            try:
                os.makedirs(self.noteBookDir)
            except OSError:
                self.info += 'Can`t create workdir at {} . '.format(self.noteBookDir)
                if platform.system() == 'Windows':
                    directory = os.path.join(os.getenv('HOMEDRIVE'), os.getenv('HOMEPATH'))
                else:
                    directory = os.getenv('HOME')
                self.__class__.set_books_dir(directory)
                self.noteBookDir = directory + os.sep + self.user
            finally:
                self.info += 'Workdir set at {} . '.format(self.noteBookDir)

    def __read_file(self, attr_file='work_file'):
        try:
            f = open(getattr(self, attr_file), 'rb')
            stored_data = pickle.load(f)
            stored_data = dict(sorted(stored_data.items()))
            f.close()
        except OSError:
            stored_data = {}
        return stored_data

    def __save_file(self, type_file='data'):
        err_dict = {}
        if type_file == 'data':
            file_name = self.work_file
            stored = self.stored_data
        elif type_file == 'cfg':
            file_name = self.cfg_file
            stored = self.stored_config
        try:
            f = open(file_name, 'wb')
            pickle.dump(stored, f)
            f.close()
            err_dict['error'] = False
        except OSError:
            err_dict['error'] = True
            err_dict['error_description'] = 'Can`t save {} file to NoteBook. Please, try again'.format(type_file)
        return err_dict

    def update_contact(self, contact, key_fields):
        '''from key_fields combines uid of contact in contact.getuid '''
        err_dict = self.empty_key_fields(contact, key_fields)
        if err_dict.get('error', False):
            return err_dict
        self.__check_fields_stored_data(contact)
        if not self.stored_config.get('key_fields', False) or self.stored_config['key_fields'] != key_fields:
            self.__update_key_fields(key_fields)
        self.stored_data[contact.get_uid(key_fields)] = contact.__dict__
        err_dict = self.__save_file('cfg')
        if err_dict.get('error', False):
            return err_dict
        return self.__save_file()

    @staticmethod
    def empty_key_fields(contact, key_fields):
        err_dict = {}
        for key_field in key_fields:
            if not getattr(contact, key_field, False):
                err_dict['error'] = True
                err_dict['error_description'] = 'It is forbidden to save empty values of key fields'
                break
            else:
                err_dict['error'] = False
        return err_dict

    def __check_fields_stored_data(self, contact):
        book_fields = self.get_book_fields()
        new_book_fields = contact.get_fields()
        if book_fields != new_book_fields:
            new_fields_list = list(set(new_book_fields) - set(book_fields))
            for value in self.stored_data.values():
                for field in new_fields_list:
                    value.update({field: ''})
            # return self.__save_file()

    def __update_key_fields(self, new_key_fields):
        self.__update_uids_stored_data(new_key_fields)
        self.stored_config['key_fields'] = new_key_fields
        # return self.__save_file('cfg')

    def __update_uids_stored_data(self, new_key_fields):
        new_stored_data = {}
        for value in self.stored_data.values():
            contact = Contacts(value)
            new_stored_data[contact.get_uid(new_key_fields)] = value
        self.stored_data = new_stored_data
        # return self.__save_file()

    def get_contact(self, uid):
        return self.stored_data.get(uid, {})

    def delete_contact(self, uid):
        contact = self.stored_data.pop(uid)
        return self.__save_file()

    def find_contacts(self, keyname='', value=''):
        if keyname == 'uid':
            return [self.get_contact(value), ]
        else:
            return [item for item in self.stored_data.values() if
                    not keyname or not value or item.get(keyname) == value]

    def find_substring_contacts(self, value):
        return [item for item in self.stored_data.values() if value.upper() in ' '.join(item.values()).upper()]

    def get_book_not_key_fields(self, key_fields=None):
        fields_set = set()
        if not key_fields:
            key_fields = self.get_book_key_fields()
        for entry in self.stored_data.values():
            for key in entry:
                if key in key_fields:
                    continue
                fields_set.add(key)
        fields_list = list(fields_set)
        fields_list.sort()
        return fields_list

    def get_book_fields(self):
        fields_set = set()
        for entry in self.stored_data.values():
            for key in entry:
                fields_set.add(key)
        fields_list = list(fields_set)
        fields_list.sort()
        return fields_list

    def get_book_key_fields(self):
        if self.stored_config.get('key_fields', False):
            key_fields = self.stored_config['key_fields']
            key_fields.sort()
        else:
            key_fields = []
        return key_fields

    def view_contacts(self):
        return self.find_contacts()
