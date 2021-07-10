#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from time import time

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt


CONFIG_FILE = 'config.json'
UI_DIR = 'ui'
DB_FILENAME = 'saved_texts.sqlite'


class AboutWindow(QDialog):
    """About dialog with some text, image and close button"""
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        uic.loadUi(UI_DIR + '/about.ui', self)
        self.setFixedSize(self.size())
        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.close_button.clicked.connect(self.close)
        self.about_field.setText('Yet another PyQT5 demo application '
                                 'made on Earth\nby humans?')
        self.author_label.setText('89dd33736a5f5ff75891479a4e633897')


class HelpWindow(QDialog):
    """Help dialog with rendered README.md on text-browser field"""
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        uic.loadUi(UI_DIR + '/help.ui', self)
        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.close_button.clicked.connect(self.close)

        readme = '(Help!) I need somebody!  \n' \
                 '(Help!) Not just anybody  \n' \
                 '(Help!) You know I need someone  \n' \
                 '\tHeelp~  \n\n'

        readme += open('README.md', 'r').read()
        self.help_field.setText(readme)
        try:
            self.help_field.setMarkdown(readme)
        except:
            pass


class TextsDB():
    """DB-interaction class"""
    def __init__(self, db_filename=DB_FILENAME):
        """Init method.
        Opens or create file-based db with required table 'texts'"""
        self.db_filename = db_filename
        self.table_name = 'texts'
        self.conn = sqlite3.connect(db_filename)
        self.cur = self.conn.cursor()
        self.init_db()

    def __del__(self):
        """Explicit is better than implicit"""
        self.conn.close()

    def init_db(self):
        """Creates 'texts' table with 3 fields:
        id - autoincremented primary key;
        text - user texts storage field;
        timestamp - timestamp of saved text"""
        sql = f'''CREATE TABLE IF NOT EXISTS `{self.table_name}` (
                    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    `text` TEXT,
                    `timestamp` INTEGER
                  )'''
        self.cur.execute(sql)
        self.conn.commit()

    def add_row(self, text, timestamp=None):
        """Inserts new user-text into table"""
        if not timestamp or not isinstance(timestamp, int):
            timestamp = int(time())

        sql = f'''INSERT INTO `{self.table_name}`(`text`,`timestamp`)
                            VALUES (?, ?);'''
        self.cur.execute(sql, (text, timestamp))
        self.conn.commit()
        return self.cur.lastrowid

    def get_row(self, id_=None):
        """Returns id-defined text from table
        or last text if id not specified"""
        if not id_:
            sql = f'''SELECT `text` FROM `{self.table_name}`
                                    ORDER BY `id` DESC LIMIT 1'''
            res = self.cur.execute(sql).fetchone()
        else:
            sql = f'''SELECT `text` FROM `{self.table_name}` WHERE `id` = ?;'''
            res = self.cur.execute(sql, (id_,)).fetchone()

        return res[0]

    def get_rows(self):
        """Returns list of (id, text)-tuples with all texts from table"""
        sql = f'''SELECT `id`, `text` FROM `{self.table_name}`;'''
        res = self.cur.execute(sql).fetchall()
        return res

    def delete_row(self, id_):
        """Deletes id-specified text from table"""
        sql = f'''DELETE FROM `{self.table_name}` WHERE `id` = ?;'''
        self.cur.execute(sql, (id_,))
        self.conn.commit()

    def clear_db(self):
        """Like DROP TABLE but more gentle"""
        sql = f'DELETE FROM `{self.table_name}`'
        self.cur.execute(sql)
        self.conn.commit()
