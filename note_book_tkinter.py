"""Description1 ..."""
import os
import tkinter.filedialog
import tkinter.messagebox as mb
import pickle
from tkinter import *
from tkinter import ttk
from note_book import NoteBook as Nb
from note_book import Contacts


class VisualNoteBook:

    def __init__(self):
        self.fields_list = []
        self.fields_list_val = []
        self.__init_root()
        self.__init_mainframe()
        self.root.mainloop()

    def __init_root(self):
        self.root = Tk()
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.bind('<Control-Return>', self.add_new_field)
        self.root.title('Work with notebooks')

    def __init_mainframe(self):
        self.mainframe = ttk.Frame(self.root, padding='3 3 12 12')  # это отступы элементов от краев этого фрейма
        self.mainframe['borderwidth'] = 2
        self.mainframe['relief'] = 'sunken'
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.__init_main_fields()

    def __init_main_fields(self):
        self.__read_settings()
        ttk.Label(self.mainframe, text='Settings').grid(column=1, row=1, columnspan=10, pady=10)
        self.row_point = 10
        self.func_dict = {'entry': ttk.Entry, 'combobox': ttk.Combobox}
        main_fields_list = list()
        main_fields_list.append(
            {'name': 'books_dir', 'type': 'entry', 'text': 'Notebooks dir', 'command': self.__change_dir,
             'command_name': 'Change dir', 'val_func': Nb.get_books_dir})

        main_fields_list.append(
            {'name': 'user_name', 'type': 'combobox', 'text': 'User name', 'command': self.__change_user,
             'command_name': ['<<ComboboxSelected>>', '<FocusOut>'], 'val_func': Nb.get_usernames})

        main_fields_list.append(
            {'name': 'book_name', 'type': 'combobox', 'text': 'Notebook name', 'command': self.__change_book,
             'command_name': ['<<ComboboxSelected>>', '<FocusOut>'], 'val_func': self.__get_books_name})

        main_fields_list.append(
            {'name': 'field_name', 'type': 'entry', 'text': 'Enter new field name', 'command': self.add_new_field,
             'command_name': 'Add field (Ctrl+Enter)', 'focus': True})

        for item in main_fields_list:
            self.__add_field(item)

        self.__add_fields_header()
        self.__refresh_users()
        self.__add_fields_footer()
        self.__init_search()

    def __read_settings(self):
        try:
            f = open('settings.cfg', 'rb')
            settings = pickle.load(f)
            f.close()
        except OSError:
            return
        if settings:
            try:
                settings_books_dir = settings['books_dir']
                if os.path.exists(settings_books_dir):
                    self.settings_user_name = settings['user_name']
                    self.settings_book_name = settings['book_name']
                    Nb.set_books_dir(settings_books_dir)
                else:
                    # settings_books_dir = os.getcwd()+
                    self.settings_user_name = settings['user_name']
                    self.settings_book_name = settings['book_name']
                    # Nb.set_books_dir(settings_books_dir)
            except:
                pass

    def __init_search(self):
        ttk.Label(self.mainframe, text='View notebook').grid(column=1, row=200, columnspan=10, pady=10)

        self.search_field = StringVar()
        self.search_field_entry = ttk.Entry(self.mainframe, textvariable=self.search_field, width=10)
        self.search_field_entry.grid(column=1, row=201, sticky=(W, E), columnspan=10)

        ttk.Button(self.mainframe, text='Find', command=self.find_records).grid(column=1, row=202, sticky=(W, E),
                                                                                columnspan=10)
        ttk.Button(self.mainframe, text='View all', command=self.view_records).grid(column=1, row=203, sticky=(W, E),
                                                                                    columnspan=10)

    def find_records(self):
        if not hasattr(self, 'book'):
            return
        self.__add_table_view()
        contact_list = self.book.find_substring_contacts(self.search_field.get())
        self.__feel_table_view(contact_list)

    def view_records(self):
        if not hasattr(self, 'book'):
            return
        self.__add_table_view()
        contact_list = self.book.view_contacts()
        self.__feel_table_view(contact_list)

    @staticmethod
    def __sort_contact_list(contact_list, columns):
        return [dict(sorted(val.items(), key=lambda item: columns.index(item[0]))) for val in contact_list]

    def __add_table_view(self):
        if hasattr(self, 'table_view'):
            self.table_view.destroy()
        # columns = self.book.get_book_fields()
        key_fields = self.book.get_book_key_fields()
        not_key_fields = self.book.get_book_not_key_fields(key_fields)
        columns = key_fields + not_key_fields
        self.table_view = ttk.Treeview(self.mainframe, columns=columns, show="headings")
        self.table_view.grid(column=1, row=300, sticky=(W, E), columnspan=10)
        scrollbar = ttk.Scrollbar(self.mainframe, orient=VERTICAL, command=self.table_view.yview)
        self.table_view.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=300, column=11, sticky=(N, S))
        for val in columns:
            self.table_view.heading(val, text=val)

    def __feel_table_view(self, contact_list):
        key_fields = self.book.get_book_key_fields()
        not_key_fields = self.book.get_book_not_key_fields(key_fields)
        columns = key_fields + not_key_fields
        sorted_contact_list = self.__sort_contact_list(contact_list, columns)
        for item in sorted_contact_list:
            self.table_view.insert('', END, values=tuple(item.values()))

    def __add_field(self, par):
        name = par['name']
        kind = par['type']
        frame = self.mainframe
        name_kind = name + '_' + kind
        if 'check' not in par.keys():
            label = ttk.Label(frame, text=par['text'], width=20)
            label.grid(column=1, row=self.row_point, sticky=W)
            setattr(self, name_kind + '_label', label)

        setattr(self, name, StringVar())
        obj = self.func_dict[kind]
        setattr(self, name_kind, obj(frame, textvariable=getattr(self, name), width=30))
        getattr(self, name_kind).grid(column=2, row=self.row_point, sticky=(W, E), columnspan=9)

        if par.get('focus', False):
            getattr(self, name_kind).focus()
        if kind == 'entry':

            if par.get('val_func', False):
                getattr(self, name).set(par['val_func']())

            if par.get('command_name', False) and par.get('command', False):
                self.row_point += 1
                ttk.Button(frame, text=par['command_name'],
                           command=par['command']).grid(column=1, row=self.row_point, sticky=(W, E), columnspan=10)

            if 'check' in par.keys():
                setattr(self, name + '_check', BooleanVar())
                getattr(self, name + '_check').set(par['check'])
                check = ttk.Checkbutton(frame, variable=getattr(self, name + '_check'), width=20, text=name,
                                        takefocus=0)
                check.grid(column=1, row=self.row_point, sticky=W)
                setattr(self, name_kind + '_check', check)

        elif par['type'] == 'combobox':

            if par.get('val_func', False):
                getattr(self, name_kind)['values'] = par['val_func']()
                if getattr(self, name_kind)['values']:
                    getattr(self, name_kind).current(0)

            if par.get('command_name', False) and par.get('command', False):
                for command_name in par['command_name']:
                    getattr(self, name_kind).bind(command_name, par['command'])
        self.row_point += 1

    def __add_fields_header(self):
        ttk.Label(self.mainframe, text='Notebook fields').grid(column=1, row=self.row_point, columnspan=10, pady=10)
        self.row_point += 1
        ttk.Label(self.mainframe, text='Field').grid(column=1, row=self.row_point, sticky=W)
        # ttk.Label(self.mainframe, text='Key', width=3).grid(column=1, row=self.row_point, sticky=E)
        ttk.Label(self.mainframe, text='Value').grid(column=2, row=self.row_point, sticky=W, columnspan=10)
        self.row_point += 1

    def __add_fields_footer(self):
        ttk.Button(self.mainframe, text='Add record', command=self.save_book).grid(column=1, row=100, sticky=(W, E),
                                                                                   columnspan=10)

    def __get_books_name(self):
        return Nb.get_books_names(self.user_name.get())

    def __change_dir(self):
        dir_name = tkinter.filedialog.askdirectory()
        if dir_name:
            Nb.set_books_dir(dir_name)
            self.books_dir.set(Nb.get_books_dir())
        self.__refresh_users()

    def __change_user(self, *args):
        self.__refresh_books_name()

    def __change_book(self, *args):
        self.__set_book()

    def __refresh_users(self):
        users_list = Nb.get_usernames()
        self.user_name_combobox['values'] = users_list
        if getattr(self, 'settings_user_name', False):
            if self.settings_user_name in users_list:
                self.user_name.set(self.settings_user_name)
            self.settings_user_name = ''
        elif not self.user_name.get() in users_list:
            self.user_name.set('')
            if self.user_name_combobox['values']:
                self.user_name_combobox.current(0)

        self.__refresh_books_name()

    def __refresh_books_name(self):
        books_list = self.__get_books_name()
        self.book_name_combobox['values'] = books_list
        if getattr(self, 'settings_book_name', False):
            if self.settings_book_name in books_list:
                self.book_name.set(self.settings_book_name)
            self.settings_book_name = ''
        elif not self.book_name.get() in books_list:
            self.book_name.set('')
            if self.book_name_combobox['values']:
                self.book_name_combobox.current(0)

        self.__set_book()

    def __set_book(self):
        settings = self.__save_settings()
        if settings.get('user_name', False) and settings.get('book_name', False):
            self.book = Nb(settings['user_name'], settings['book_name'])
            self.books_dir.set(Nb.get_books_dir())
            if self.book.info:
                self.__show_info(self.book.info)
            self.root.title('User "{}", notebook "{}"'.format(settings['user_name'], settings['book_name']))
        else:
            if hasattr(self, 'book'):
                del self.book

        self.__refresh_book_fields()

    def __save_settings(self):
        try:
            settings = {'books_dir': self.books_dir.get(), 'user_name': self.user_name.get(),
                        'book_name': self.book_name.get()}
            f = open('settings.cfg', 'wb')
            pickle.dump(settings, f)
            f.close()
        except OSError:
            settings = {}

        return settings

    def __refresh_book_fields(self):
        # self.__take_focus_off_book_fields()
        self.__delete_book_fields()
        self.__add_book_fields()
        # self.__take_focus_off_book_fields()
        # self.__add_fields_footer()
        # self.__init_search()

    def __take_focus_off_book_fields(self):
        for item in self.fields_list:
            self.__take_focus_off_book_field(getattr(self, item))
            self.__take_focus_off_book_field(getattr(self, item + '_check'))

    def __take_focus_off_book_field(self, item):
        item['takefocus'] = 0

    def __delete_book_fields(self):
        for item in self.fields_list:
            it = getattr(self, item)
            it1 = getattr(self, item + '_check')
            self.root.after(0, it.destroy)  # forget()
            self.root.after(0, it1.destroy)  # forget()
            # getattr(self, item + '_label').destroy()
            self.row_point -= 1
        self.fields_list = []
        self.fields_list_val = []

    def __add_book_fields(self):
        if not hasattr(self, 'book'):
            return
        key_fields = self.book.get_book_key_fields()
        not_key_fields = self.book.get_book_not_key_fields(key_fields)
        for field in key_fields:
            self.__add_book_field(field, True)
        for field in not_key_fields:
            self.__add_book_field(field, False)
        self.__add_table_view()

    def __add_book_field(self, field, key):
        field_dict = {'name': field, 'type': 'entry', 'text': field + ': ', 'check': key}
        self.__add_field(field_dict)
        self.fields_list.append(field + '_entry')
        self.fields_list_val.append(field)

    def add_new_field(self, *args):
        self.field_name_entry.focus()
        field_name = self.field_name.get()
        if field_name == '':
            return
        if self.name_is_exist(field_name):
            self.__show_info('Field "{}" is exist'.format(field_name))
            return
        self.__add_book_field(field_name, False)

        self.field_name.set('')

    @staticmethod
    def __show_info(msg):
        mb.showinfo("Информация", msg)

    @staticmethod
    def __show_error(msg):
        mb.showerror("Ошибка", msg)

    def name_is_exist(self, name):
        return name + '_entry' in self.fields_list

    def save_book(self):
        contact_dict = {val: getattr(self, val).get() for val in self.fields_list_val}
        key_fields = [value for value in self.fields_list_val if getattr(self, value + '_check').get()]
        key_fields.sort()
        contact = Contacts(contact_dict)
        result_dict = self.book.update_contact(contact, key_fields)
        if result_dict.get('error', False):
            self.__show_error(result_dict.get('error_description', ''))

        for val in self.fields_list_val:
            getattr(self, val).set('')
