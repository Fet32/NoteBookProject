"""."""
from tkinter.ttk import Frame, Label, Combobox, Widget
from tkinter import constants, messagebox, StringVar

from typing import Type

from note_book import NoteBook


class BaseFrame(Frame):

    def __init__(self, master, padding, config):
        super().__init__(master=master, padding=padding)
        self.config = config

    def grid_frame(self, grid_row, frame_columns_count, frame_rows_count):

        self.grid(column=0, row=grid_row)

        for i in range(frame_columns_count):
            self.grid_columnconfigure(i, weight=1, minsize=150)

        for i in range(frame_rows_count):
            self.grid_rowconfigure(i, weight=1, minsize=21)

    def show_info(self, msg: str):
        messagebox.showerror('Error', msg)

    def init_combobox(self, name: str, column: int, row: int, text_var: StringVar, values: list):
        widget = Combobox(
            master=self,
            textvariable=text_var,
            name=name,
            width=1030,
            values=values,
        )
        widget.grid(column=column, row=row, sticky=constants.EW)
        if widget['values']:
            widget.current(0)

        #widget.bind('<<ComboboxSelected>>', self._change_user)
        #widget.bind('<FocusOut>', self._change_user)

        return widget

    def init_label(self, text: str, column: int, row: int):
        label = Label(self, text=text, width=20)
        label.grid(column=column, row=row, sticky=constants.W)


class BookFrame(BaseFrame):

    def __init__(self, master, padding, config):
        super().__init__(master=master, padding=padding, config=config)

        self.init_label(text='User name', column=0, row=0)
        self.user_name_combobox = self.init_combobox(
            name='user_name_combobox',
            column=0,
            row=1,
            text_var=self.config.user_name,
            values=NoteBook.get_usernames(),
        )

        self.init_label(text='Notebook name', column=0, row=1)
        self.book_name_combobox = self.init_combobox(
            name='book_name_combobox',
            column=1,
            row=1,
            text_var=self.config.book_name,
            values=NoteBook.get_books_names(
                self.config.user_name.get(),
            ),
        )

        self.grid_frame(1, 2, 1)

        if self.config.user_name and not NoteBook.check_user_existence(self.config.user_name.get()):
            self.show_info(
                'Don`t find user {} from last settings'.format(self.config.user_name.get()),
            )
            self.config.user_name.set('')
