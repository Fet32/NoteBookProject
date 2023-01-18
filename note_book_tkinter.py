"""Description1 ..."""
import json
from tkinter import constants, ttk, messagebox, filedialog, Tk, StringVar, BooleanVar
from note_book import NoteBook
from note_book import Contacts


class VisualNoteBook:

    def __init__(self):

        self.frame_dir = None
        self.frame_settings = None
        self.frame_fields_header = None
        self.frame_book_fields = None
        self.frame_search = None
        self.frame_book_table_view = None

        self.settings = self._read_settings()

        self.books_dir = ''
        self.user_name = ''
        self.book_name = ''
        self.field_name = ''
        self.dict_fields = {}

        self.root = self._init_root()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self._init_frames()

        self.root.mainloop()

    @staticmethod
    def _read_settings():
        try:
            with (open('last_settings.json', 'r')) as file_d:
                return json.load(file_d)
        except:
            return {}

    def on_closing(self):
        self._save_settings()
        self.root.destroy()

    def _save_settings(self):
        try:
            settings = {
                'books_dir': self.books_dir.get(),
                'user_name': self.user_name.get(),
                'book_name': self.book_name.get()
            }

            with (open('last_settings.json', 'w')) as file_d:
                json.dump(settings, file_d)

        except Exception as inst:
            self._show_info(str(inst))

    def _init_root(self):
        root = Tk()

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        root.rowconfigure(2, weight=1)
        root.rowconfigure(3, weight=1)
        root.rowconfigure(4, weight=1)
        root.rowconfigure(5, weight=1)
        root.rowconfigure(6, weight=1)

        root['borderwidth'] = 2
        root['relief'] = 'sunken'

        root.title('Work with notebooks')
        root.resizable = True
        root.bind('<Control-Return>', self.add_new_field)
        return root

    def _init_frames(self):
        self.frame_dir = self._create_frame_books_dir()
        self.frame_dir.grid(column=0, row=0)
        self.frame_dir.columnconfigure(0, weight=1)

        self.frame_settings = self._create_frame_book_settings()
        self.frame_settings.grid(column=0, row=1)

        self._init_settings()

        self.frame_fields_header = self._create_frame_book_fields_header()
        self.frame_fields_header.grid(column=0, row=3)

        self.frame_book_fields = self._create_frame_book_fields()
        self.frame_book_fields.grid(column=0, row=4)

        self.frame_search = self._create_frame_book_search()
        self.frame_search.grid(column=0, row=5)

        self.frame_book_table_view = self._create_frame_table_view()
        self.frame_book_table_view.grid(column=0, row=6)

    def _init_settings(self):
        self._init_settings_books_dir()
        self._init_settings_users()
        self._init_settings_books()
        self._initialize_book()

    def _init_settings_books_dir(self):
        if self.settings.get('books_dir', False):
            NoteBook.set_books_dir(self.settings['books_dir'])
            self.books_dir.set(NoteBook.get_books_dir())

    def _init_settings_users(self):
        users_list = NoteBook.get_usernames()
        self.frame_settings.children.get('user_name_combobox')['values'] = users_list

        if self.settings.get('user_name', False):
            if self.settings['user_name'] in users_list:
                self.user_name.set(self.settings['user_name'])
            else:
                self._show_info('Don`t find user {} from last settings'.format(self.settings['user_name']))

    def _init_settings_books(self):
        books_list = self._get_books_name()
        self.frame_settings.children.get('book_name_combobox')['values'] = books_list

        if self.settings.get('book_name', False):
            if self.settings['book_name'] in books_list:
                self.book_name.set(self.settings['book_name'])
            else:
                self._show_info('Don`t find book with name {} from last settings'.format(self.settings['book_name']))

    def _create_frame_books_dir(self):
        """Create frame for books_dir."""
        frame = ttk.Frame(self.root, padding='3 3 12 12')

        label = ttk.Label(frame, text='Settings')
        label.grid(column=0, row=0, columnspan=10, pady=10)

        label = ttk.Label(frame, text='Notebooks dir', width=20)
        label.grid(column=0, row=1, sticky=constants.W)

        # name_kind = 'books_dir_entry'
        # setattr(self, name_kind + '_label', label)  # TODO will be removed

        var = StringVar()
        widget = ttk.Entry(master=frame, textvariable=var, width=30)
        widget.grid(column=1, row=1, sticky=constants.EW, columnspan=9)

        var.set(NoteBook.get_books_dir())
        self.books_dir = var  # TODO will be removed

        button = ttk.Button(master=frame, text='Change dir', command=self._change_dir)
        button.grid(column=0, row=2, sticky=constants.NSEW, columnspan=10)

        return frame

    def _create_frame_book_settings(self):
        """Create frame for settings with username, book name"""
        frame = ttk.Frame(self.root, padding='3 3 12 12')

        label = ttk.Label(frame, text='User name', width=20)
        label.grid(column=0, row=1, sticky=constants.W)

        var = StringVar()
        self.user_name = var  # TODO will be removed

        widget = ttk.Combobox(master=frame, textvariable=var, name='user_name_combobox', width=30,
                              values=NoteBook.get_usernames())
        widget.grid(column=1, row=1, sticky=constants.EW, columnspan=9)
        if widget['values']:
            widget.current(0)

        widget.bind('<<ComboboxSelected>>', self._change_user)
        widget.bind('<FocusOut>', self._change_user)

        label = ttk.Label(frame, text='Notebook name', width=20)
        label.grid(column=0, row=2, sticky=constants.W)

        var = StringVar()
        self.book_name = var  # TODO will be removed

        widget = ttk.Combobox(master=frame, textvariable=var, name='book_name_combobox', width=30,
                              values=self._get_books_name())
        widget.grid(column=1, row=2, sticky=constants.EW, columnspan=9)
        if widget['values']:
            widget.current(0)

        widget.bind('<<ComboboxSelected>>', self._change_book)
        widget.bind('<FocusOut>', self._change_book)

        return frame

    def _create_frame_book_fields_header(self):
        """Create frame with button to create a new field and headers of fields"""
        frame = ttk.Frame(self.root, padding='3 3 12 12')

        label = ttk.Label(frame, text='Enter new field name', width=20)
        label.grid(column=0, row=0, sticky=constants.W)

        var = StringVar()
        self.field_name = var  # TODO will be removed

        widget = ttk.Entry(master=frame, textvariable=var, width=30, name='field_name_entry')
        widget.grid(column=1, row=0, sticky=constants.EW, columnspan=9)
        widget.focus()

        button = ttk.Button(master=frame, text='Add field (Ctrl+Enter)', command=self.add_new_field)
        button.grid(column=0, row=1, sticky=constants.EW, columnspan=10)

        label = ttk.Label(frame, text='Notebook fields')
        label.grid(column=0, row=2, columnspan=10, pady=10)

        label = ttk.Label(frame, text='Field')
        label.grid(column=0, row=3, sticky=constants.W)

        label = ttk.Label(frame, text='Value')
        label.grid(column=1, row=3, sticky=constants.W, columnspan=10)

        return frame

    def _refresh_frame_book_fields(self):
        self._delete_frame_book_fields()
        return self._create_frame_book_fields()

    def _delete_frame_book_fields(self):
        if getattr(self, 'frame_book_fields', False):
            self.frame_book_fields.destroy()

    def _create_frame_book_fields(self):
        """Create frame with fields of choosen book and button to create a new field"""

        frame = ttk.Frame(self.root, padding='3 3 12 12')

        if not hasattr(self, 'book'):
            return frame

        key_fields = self.book.get_book_key_fields()
        not_key_fields = self.book.get_book_not_key_fields(key_fields)
        row_point = 0

        for field_name in key_fields:
            self._add_book_field(frame, field_name, row_point, True)
            row_point += 1

        for field_name in not_key_fields:
            self._add_book_field(frame, field_name, row_point, False)
            row_point += 1

        button = ttk.Button(frame, text='Add record', command=self.save_book)
        button.grid(column=0, row=row_point, sticky=constants.EW, columnspan=10)

        return frame

    def _add_book_field(self, frame: ttk.Frame, name: str, row_point, check: bool):

        key_var = BooleanVar()
        key_var.set(check)
        # setattr(self, name + '_check', check_var)  # TODO will be removed
        widget = ttk.Checkbutton(frame, variable=key_var, width=20, text=name, takefocus=0,
                                 command=self._change_key_field)
        widget.grid(column=0, row=row_point, sticky=constants.W)

        var = StringVar()
        # setattr(self, name, var)  # TODO will be removed
        widget = ttk.Entry(frame, textvariable=var, width=30)
        widget.grid(column=1, row=row_point, sticky=constants.EW, columnspan=9)

        self.dict_fields.update({name: (var, key_var)})

    def _change_key_field(self):
        self._update_book_key_field()
        self._refresh_book_frames()

    def _update_book_key_field(self):
        if not hasattr(self, 'book'):
            return

        key_fields = [item[0] for item in self.dict_fields.items() if item[1][1].get()]
        key_fields.sort()

        result_dict = self.book.update_key_fields(key_fields, True)
        if result_dict.get('error', False):
            self._show_error(result_dict.get('error_description', ''))

    # def _init_main_fields(self):

    # main_fields_list = list()

    # main_fields_list.append(
    #    {'name': 'books_dir', 'type': 'entry', 'text': 'Notebooks dir', 'command': self._change_dir,
    #     'command_name': 'Change dir', 'val_func': Nb.get_books_dir})

    # main_fields_list.append(
    #     {'name': 'user_name', 'type': 'combobox', 'text': 'User name', 'command': self._change_user,
    #      'command_name': ['<<ComboboxSelected>>', '<FocusOut>'], 'val_func': Nb.get_usernames})
    #
    # main_fields_list.append(
    #     {'name': 'book_name', 'type': 'combobox', 'text': 'Notebook name', 'command': self._change_book,
    #      'command_name': ['<<ComboboxSelected>>', '<FocusOut>'], 'val_func': self._get_books_name})

    # main_fields_list.append(
    #     {'name': 'field_name', 'type': 'entry', 'text': 'Enter new field name', 'command': self.add_new_field,
    #      'command_name': 'Add field (Ctrl+Enter)', 'focus': True})

    # self._create_frame_books_dir()

    # for item in main_fields_list:
    #     self._add_field(item)

    # self._add_fields_header()
    # self._add_fields_footer()
    # self._init_search()

    def _create_frame_book_search(self):
        frame = ttk.Frame(self.root, padding='3 3 12 12')

        label = ttk.Label(frame, text='View notebook')
        label.grid(column=0, row=0, columnspan=10, pady=10)

        var = StringVar()
        # self.search_field = var  # TODO will be removed

        widget = ttk.Entry(frame, textvariable=var, width=10, name='search_field_entry')
        widget.grid(column=0, row=1, sticky=constants.EW, columnspan=10)

        button = ttk.Button(frame, text='Find', command=self.find_records)
        button.grid(column=0, row=2, sticky=constants.EW, columnspan=10)

        button = ttk.Button(frame, text='View all', command=self.view_records)
        button.grid(column=0, row=3, sticky=constants.EW, columnspan=10)

        return frame

    def _refresh_frame_table_view(self):
        self._delete_frame_table_view()
        return self._create_frame_table_view()

    def _delete_frame_table_view(self):
        if getattr(self, 'frame_table_view', False):
            self.frame_book_table_view.destroy()

    def _create_frame_table_view(self):
        frame = ttk.Frame(self.root, padding='3 3 12 12')

        if not hasattr(self, 'book'):
            return frame

        key_fields = self.book.get_book_key_fields()
        not_key_fields = self.book.get_book_not_key_fields(key_fields)
        columns = key_fields + not_key_fields

        widget = ttk.Treeview(frame, columns=columns, show="headings", name='table_view')
        widget.grid(column=0, row=0, sticky=constants.EW, columnspan=10)

        scrollbar = ttk.Scrollbar(frame, orient=constants.VERTICAL, command=widget.yview)
        widget.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=11, sticky=constants.NS)

        for val in columns:
            widget.heading(val, text=val)

        return frame

    def find_records(self):
        if not hasattr(self, 'book'):
            return

        search_value = self.frame_search.children.get('search_field_entry').get()
        contact_list = self.book.find_substring_contacts(search_value) #self.search_field.get())
        self._feel_table_view(contact_list)

    def view_records(self):
        if not hasattr(self, 'book'):
            return
        contact_list = self.book.view_contacts()
        self._feel_table_view(contact_list)

    @staticmethod
    def _sort_contact_list(contact_list, columns):
        '''contact_list - list of dictionaries.
        Function sorted each dictionary in contact_list in order from columns'''
        return [dict(sorted(val.items(), key=lambda item: columns.index(item[0]))) for val in contact_list]

    def _feel_table_view(self, contact_list):
        table_view = self.frame_book_table_view.children.get('table_view')

        self._clear_table_view(table_view)

        key_fields = self.book.get_book_key_fields()
        columns = key_fields + self.book.get_book_not_key_fields(key_fields)

        sorted_contact_list = self._sort_contact_list(contact_list, columns)

        for item in sorted_contact_list:
            table_view.insert('', constants.END, values=tuple(item.values()))

    @staticmethod
    def _clear_table_view(table_view):
        for i in table_view.get_children():
            table_view.delete(i)

    # def _add_field(self, par):
    #     name = par['name']
    #     kind = par['type']
    #     frame = self.mainframe
    #     name_kind = name + '_' + kind
    #     if 'check' not in par.keys():
    #         label = ttk.Label(frame, text=par['text'], width=20)
    #         label.grid(column=1, row=self.row_point, sticky=constants.W)
    #         setattr(self, name_kind + '_label', label)
    #
    #     setattr(self, name, StringVar())
    #     obj = self.func_dict[kind]
    #     setattr(self, name_kind, obj(frame, textvariable=getattr(self, name), width=30))
    #     getattr(self, name_kind).grid(column=2, row=self.row_point, sticky=constants.EW, columnspan=9)
    #
    #     if par.get('focus', False):
    #         getattr(self, name_kind).focus()
    #     if kind == 'entry':
    #
    #         if par.get('val_func', False):
    #             getattr(self, name).set(par['val_func']())
    #
    #         if par.get('command_name', False) and par.get('command', False):
    #             self.row_point += 1
    #             ttk.Button(frame, text=par['command_name'],
    #                        command=par['command']).grid(column=1, row=self.row_point, sticky=constants.EW,
    #                                                     columnspan=10)
    #
    #         if 'check' in par.keys():
    #             setattr(self, name + '_check', BooleanVar())
    #             getattr(self, name + '_check').set(par['check'])
    #             check = ttk.Checkbutton(frame, variable=getattr(self, name + '_check'), width=20, text=name,
    #                                     takefocus=0)
    #             check.grid(column=1, row=self.row_point, sticky=constants.W)
    #             setattr(self, name_kind + '_check', check)
    #
    #     elif par['type'] == 'combobox':
    #
    #         if par.get('val_func', False):
    #             getattr(self, name_kind)['values'] = par['val_func']()
    #             if getattr(self, name_kind)['values']:
    #                 getattr(self, name_kind).current(0)
    #
    #         if par.get('command_name', False) and par.get('command', False):
    #             for command_name in par['command_name']:
    #                 getattr(self, name_kind).bind(command_name, par['command'])
    #     self.row_point += 1

    # def _add_fields_header(self):
    #     ttk.Label(self.mainframe, text='Notebook fields').grid(column=1, row=self.row_point, columnspan=10, pady=10)
    #     self.row_point += 1
    #     ttk.Label(self.mainframe, text='Field').grid(column=1, row=self.row_point, sticky=constants.W)
    #     # ttk.Label(self.mainframe, text='Key', width=3).grid(column=1, row=self.row_point, sticky=E)
    #     ttk.Label(self.mainframe, text='Value').grid(column=2, row=self.row_point, sticky=constants.W, columnspan=10)
    #     self.row_point += 1

    # def _add_fields_footer(self):
    #     ttk.Button(self.mainframe, text='Add record', command=self.save_book).grid(column=1, row=100,
    #                                                                                sticky=constants.EW,
    #                                                                                columnspan=10)

    def _get_books_name(self):
        return NoteBook.get_books_names(self.user_name.get())

    def _change_dir(self):
        dir_name = filedialog.askdirectory()
        if dir_name:
            NoteBook.set_books_dir(dir_name)
            self.books_dir.set(NoteBook.get_books_dir())
        self._refresh_users()

    def _change_user(self, *args):
        self._refresh_books_name()

    def _change_book(self, *args):
        self._initialize_book()
        self._refresh_book_frames()

    def _refresh_book_frames(self):
        self.frame_book_fields = self._refresh_frame_book_fields()
        self.frame_book_fields.grid(column=0, row=4, sticky=constants.NSEW)

        self.frame_book_table_view = self._refresh_frame_table_view()
        self.frame_book_table_view.grid(column=0, row=6, sticky=constants.NSEW)

    def _refresh_users(self):
        users_list = NoteBook.get_usernames()

        user_name_combobox = self.frame_settings.children.get('user_name_combobox')
        user_name_combobox['values'] = users_list

        if not self.user_name.get() in users_list:
            self.user_name.set('')

            if user_name_combobox['values']:
                user_name_combobox.current(0)

        self._refresh_books_name()

    def _refresh_books_name(self):
        books_list = self._get_books_name()

        book_name_combobox = self.frame_settings.children.get('book_name_combobox')
        book_name_combobox['values'] = books_list

        if not self.book_name.get() in books_list:
            self.book_name.set('')

            if book_name_combobox['values']:
                book_name_combobox.current(0)

        self._change_book()

    def _initialize_book(self):

        self.dict_fields = {}

        user_name = self.user_name.get()
        book_name = self.book_name.get()

        if user_name and book_name:

            self.book = NoteBook(user_name, book_name)
            self.books_dir.set(NoteBook.get_books_dir())

            if self.book.info:
                self._show_info(self.book.info)

            self.root.title('User "{}", notebook "{}"'.format(user_name, book_name))

        else:
            if hasattr(self, 'book'):
                del self.book

        # self._refresh_book_fields()
        # self.frame_book_fields = self._refresh_frame_book_fields()
        # self.frame_book_fields.grid(column=0, row=4, sticky=constants.NSEW)
        #
        # self.frame_table_view = self._refresh_frame_table_view()
        # self.frame_table_view.grid(column=0, row=6, sticky=constants.NSEW)

    # def _refresh_book_fields(self):
    #     # self._take_focus_off_book_fields()
    #     self._delete_book_fields()
    #     self._add_book_fields()
    #     # self._take_focus_off_book_fields()
    #     # self._add_fields_footer()
    #     # self._init_search()

    # def _take_focus_off_book_fields(self):
    #     for item in self.fields_list:
    #         self._take_focus_off_book_field(getattr(self, item))
    #         self._take_focus_off_book_field(getattr(self, item + '_check'))

    # def _take_focus_off_book_field(self, item):
    #     item['takefocus'] = 0

    # def _delete_book_fields(self):
    #     for item in self.fields_list:
    #         it = getattr(self, item)
    #         it1 = getattr(self, item + '_check')
    #         self.root.after(0, it.destroy)  # forget()
    #         self.root.after(0, it1.destroy)  # forget()
    #         # getattr(self, item + '_label').destroy()
    #         self.row_point -= 1
    #     self.fields_list = []
    #     self.fields_list_val = []

    # def _add_book_fields(self):
    #     if not hasattr(self, 'book'):
    #         return
    #     key_fields = self.book.get_book_key_fields()
    #     not_key_fields = self.book.get_book_not_key_fields(key_fields)
    #     for field in key_fields:
    #         self._add_book_field(field, True)
    #     for field in not_key_fields:
    #         self._add_book_field(field, False)
    #     self._add_table_view()

    # def _add_book_field(self, field, key):
    #     field_dict = {'name': field, 'type': 'entry', 'text': field + ': ', 'check': key}
    #     self._add_field(field_dict)
    #     self.fields_list.append(field + '_entry')
    #     self.fields_list_val.append(field)

    def add_new_field(self, *args):
        field_name_entry = self.frame_fields_header.children.get('field_name_entry')
        field_name = field_name_entry.get()

        if field_name == '':
            return

        if self.name_is_exist(field_name, True):
            return

        if not self._add_new_book_field(field_name):
            return

        self._refresh_book_frames()

        self.field_name.set('')
        field_name_entry.focus()

    def _add_new_book_field(self, new_field_name):
        if not hasattr(self, 'book'):
            return

        # empty contact_dict for only update fields of the book
        contact_dict = {item[0]: '' for item in self.dict_fields.items()}
        contact_dict.update({new_field_name: ''})

        contact = Contacts(contact_dict)
        result_dict = self.book.update_book_fields(contact, True)

        if result_dict.get('error', False):
            self._show_error(result_dict.get('error_description', ''))
            return False
        else:
            return True

    @staticmethod
    def _show_info(msg: str):
        messagebox.showinfo("Информация", msg)

    @staticmethod
    def _show_error(msg: str):
        messagebox.showerror("Ошибка", msg)

    def name_is_exist(self, name: str, show_info = False):
        if self.frame_book_fields.children.get(name):
            if show_info:
                self._show_info('Field "{}" is exist'.format(name))
            return True
        else:
            return False

        # return name + '_entry' in self.fields_list

    def save_book(self):
        if not hasattr(self, 'book'):
            return

        contact_dict = {}
        key_fields = []

        for item in self.dict_fields.items():

            contact_dict.update({item[0]: item[1][0].get()})
            item[1][0].set('')

            if item[1][1].get():
                key_fields.append(item[0])

        key_fields.sort()

        contact = Contacts(contact_dict)
        result_dict = self.book.update_contact(contact, key_fields)

        if result_dict.get('error', False):
            self._show_error(result_dict.get('error_description', ''))
