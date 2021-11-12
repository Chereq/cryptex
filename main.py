#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import hashlib
from inspect import signature
import json
import ctypes

# from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDialog,
                             QFileDialog, QAction)
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt, QSignalMapper, QTranslator, pyqtSlot, QEvent

from misc import (AboutWindow, HelpWindow, TextsDB,
                  CONFIG_FILE, UI_DIR)
from ui.main import Ui_MainWindow
import coders


class MainWindow(QMainWindow, Ui_MainWindow):
    """main window defines here"""
    def __init__(self):
        """init ui and connect some callbacks"""
        super().__init__()
        # uic.loadUi(UI_DIR + '/main.ui', self)
        self.setupUi(self)

        self.trans = QTranslator(self)
        self.change_lang(UI_DIR + '/eng-ru')
        # self.change_lang()

        self.hide_error()
        self.load_params()

        self.tdb = TextsDB()

        self.convert_button.clicked.connect(self.convert)
        self.radio_encode.toggled.connect(self.switch_mode_callback)
        self.radio_decode.toggled.connect(self.switch_mode_callback)
        self.radio_hash.toggled.connect(self.switch_mode_callback)
        self.coding_selector.currentTextChanged\
            .connect(self.switch_algorithm_callback)

        self.coders_list = coders.CODERS
        self.decoders_list = coders.DECODERS
        hash_algs = hashlib.algorithms_available
        self.hashes_list = [str(hs) for hs in sorted(hash_algs)]

        self.save_filename = ''

        self.about_dialog = AboutWindow(parent=self)
        self.menu_about.triggered.connect(self.about_dialog.show)

        self.help_dialog = HelpWindow(parent=self)
        self.menu_help.setShortcuts(QKeySequence('Ctrl+H'))
        self.menu_help.triggered.connect(self.help_dialog.show)

        self.actionNew.setShortcuts(QKeySequence('Ctrl+N'))
        self.actionNew.triggered.connect(self.new_file)
        self.actionOpen.setShortcuts(QKeySequence('Ctrl+O'))
        self.actionOpen.triggered.connect(self.open_file)
        self.actionSave.setShortcuts(QKeySequence('Ctrl+S'))
        self.actionSave.triggered.connect(self.save_file)
        self.actionSave_As.setShortcuts(QKeySequence('Ctrl+Shift+S'))
        self.actionSave_As.triggered.connect(lambda e: self.save_file(True))
        self.actionExit.setShortcuts(QKeySequence('Ctrl+Q'))
        self.actionExit.triggered.connect(self.close)

        self.actionCut.setShortcuts(QKeySequence('Ctrl+X'))
        self.actionCut.triggered.connect(self.text_field.cut)
        self.actionCopy.setShortcuts(QKeySequence('Ctrl+C'))
        self.actionCopy.triggered.connect(self.text_field.copy)
        self.actionPaste.setShortcuts(QKeySequence('Ctrl+V'))
        self.actionPaste.triggered.connect(self.text_field.paste)
        self.actionClear.setShortcuts(QKeySequence('Ctrl+Backspace'))
        self.actionClear.triggered.connect(self.text_field.clear)

        self.actionDBSave.triggered.connect(self.db_save_text)
        self.actionDBLoadLast.triggered.connect(self.db_load_text)

        self.window_title = self.windowTitle()

        self.update_recent_menu()
        self.db_update_menu()

        if os.name == 'nt':
            # some Шindows black magic here
            # setting taskbar icon
            myappid = 'mycompany.myproduct.subproduct.version'
            ctypes.windll.shell32\
                .SetCurrentProcessExplicitAppUserModelID(myappid)

        if 'last_mode' not in self.params or \
           self.params['last_mode'] == 'encode':
            self.radio_encode.setChecked(True)
        elif self.params['last_mode'] == 'decode':
            self.radio_decode.setChecked(True)
        else:
            self.radio_hash.setChecked(True)

    def change_lang(self, lang=None):
        if lang:
            self.trans.load(lang)
            QApplication.instance().installTranslator(self.trans)
        else:
            QApplication.instance().removeTranslator(self.trans)

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            self.retranslateUi(self)
        super().changeEvent(event)

    def db_update_menu(self):
        """Update load-text menu with texts list from db"""
        self.menuLoad_text.clear()
        clear_DBAction = QAction("Clear items", self)
        clear_DBAction.triggered.connect(self.db_clear)
        clear_DBAction.setEnabled(False)
        self.actionDBLoadLast.setEnabled(False)

        self.db_mapper = QSignalMapper(self)

        for text in self.tdb.get_rows():
            action_name = text[1]
            action_id = str(text[0])
            if len(action_name) >= 15:
                action_name = action_name[:15] + '...'
            DBAction = QAction(action_name, self)
            self.menuLoad_text.addAction(DBAction)
            self.db_mapper.setMapping(DBAction, action_id)
            DBAction.triggered.connect(self.db_mapper.map)
            clear_DBAction.setEnabled(True)
            self.actionDBLoadLast.setEnabled(True)

        self.db_mapper.mapped['QString'].connect(self.db_load_text)
        self.menuLoad_text.addSeparator()
        self.menuLoad_text.addAction(clear_DBAction)

    def db_clear(self, event):
        """Clear db and update load-text menu"""
        self.tdb.clear_db()
        self.db_update_menu()

    def db_load_text(self, event):
        """Load last or id-defined text from db"""
        if event:
            text = self.tdb.get_row(int(event))
        else:
            text = self.tdb.get_row()
        self.text_field.setPlainText(text)

    def db_save_text(self, event):
        """Save text into db as new record"""
        text = self.text_field.toPlainText()
        self.tdb.add_row(text)
        self.db_update_menu()

    def clear_recent(self, event):
        """Reset recent files dictionary"""
        self.params['recent_files'].clear()
        self.update_recent_menu()

    def open_recent(self, event):
        """Open recent click callback"""
        self.open_file(self.params['recent_files'][event])

    def update_recent_menu(self):
        """Update open recent menu with files list from params"""
        self.menuOpen_recent.clear()
        clear_recentAction = QAction("Clear items", self)
        clear_recentAction.triggered.connect(self.clear_recent)
        clear_recentAction.setEnabled(False)

        self.recent_mapper = QSignalMapper(self)

        for file_name in self.params['recent_files']:
            recentAction = QAction(file_name, self)
            self.menuOpen_recent.addAction(recentAction)
            self.recent_mapper.setMapping(recentAction, file_name)
            recentAction.triggered.connect(self.recent_mapper.map)
            clear_recentAction.setEnabled(True)

        self.recent_mapper.mapped['QString'].connect(self.open_recent)
        self.menuOpen_recent.addSeparator()
        self.menuOpen_recent.addAction(clear_recentAction)

    def new_file(self):
        """Reset previously opened/saved filename and cleans text_field"""
        self.save_filename = ''
        self.text_field.clear()
        self.setWindowTitle(self.window_title)

    def open_file(self, file_name=None):
        """Open file function.
        Show file selection dialog if file_name not set,
        reads file and place file content to text area

        Args:
            file_name: Text string defines filename to open.

        """
        dir_path = os.path.abspath(os.getcwd())
        if 'save_dir' in self.params:
            dir_path = self.params['save_dir']
        if not file_name:
            file_name = QFileDialog.getOpenFileName(self,
                                                    'Open file',
                                                    dir_path)[0]
        if file_name:
            self.save_filename = file_name
            self.params['save_dir'] = os.path.dirname(
                os.path.abspath(self.save_filename))
            try:
                text = open(self.save_filename, 'r').read()
                self.text_field.setPlainText(text)
                self.setWindowTitle(self.window_title + ': ' +
                                    self.save_filename)

                basename = os.path.basename(self.save_filename)
                self.params['recent_files'][basename] = self.save_filename
                self.update_recent_menu()
            except Exception as ex:
                self.show_error(ex.__class__.__name__, str(ex))

    def save_file(self, newfile=False):
        """Save file function.
        Calls by "file" menu or hotkeys
        Save text from text area to previously selected file or
        new file by file dialog

        Args:
            newfile: bool type argument forces showing file dialog.

        """
        file_name = ''
        dir_path = os.path.abspath(os.getcwd())
        if 'save_dir' in self.params:
            dir_path = self.params['save_dir']
        if not self.save_filename or newfile:
            file_name = QFileDialog.getSaveFileName(self,
                                                    'Save file',
                                                    dir_path)[0]
        if file_name:
            self.save_filename = file_name
        if (newfile and not file_name) or \
           (not file_name and not self.save_filename):
            return
        self.params['save_dir'] = os.path.dirname(
            os.path.abspath(self.save_filename))
        basename = os.path.basename(self.save_filename)
        self.params['recent_files'][basename] = self.save_filename
        self.update_recent_menu()
        text = self.text_field.toPlainText()
        try:
            open(self.save_filename, 'w').write(text)
            self.setWindowTitle(self.window_title + ': ' +
                                self.save_filename)
        except Exception as ex:
            self.show_error(ex.__class__.__name__, str(ex))

    def closeEvent(self, event):
        """close child forms and save self form dimensions
        and some another params

        """
        self.about_dialog.close()
        self.help_dialog.close()
        self.save_params()

    def save_params(self):
        """serialize params dict and write to pretty .json file"""
        self.params['maximazed'] = self.isMaximized()
        if not self.params['maximazed']:
            self.params['geometry'] = self.geometry().getRect()

        with open(CONFIG_FILE, 'w') as fp:
            json.dump(self.params, fp, sort_keys=True, indent=4)

    def load_params(self):
        """trying to read params from .json file and
        set main window dimensions if available

        """
        try:
            with open(CONFIG_FILE, 'r') as fp:
                self.params = json.load(fp)
        except FileNotFoundError:
            self.params = dict()
        if 'recent_files' not in self.params:
            self.params['recent_files'] = dict()
        if 'geometry' in self.params:
            self.setGeometry(*self.params['geometry'])
        if 'maximazed' in self.params and self.params['maximazed']:
            self.showMaximized()

    def switch_mode_callback(self, event):
        """process clicks on radiobuttons"""
        if self.radio_encode.isChecked():
            self.set_drop_down_coders()
            self.params['last_mode'] = 'encode'
        elif self.radio_decode.isChecked():
            self.set_drop_down_decoders()
            self.params['last_mode'] = 'decode'
        elif self.radio_hash.isChecked():
            self.set_drop_down_hashes()
            self.params['last_mode'] = 'hash'

    def switch_algorithm_callback(self, event):
        """process drop-down menu select"""
        self.hile_key_spin()
        self.hile_key_field()

        if self.radio_encode.isChecked() and event in self.coders_list:
            self.params['last_coder'] = event
            if coders.is_key(event) == coders.KEY_DECIMAL:
                self.show_key_spin()
            elif coders.is_key(event) == coders.KEY_TEXT:
                self.show_key_field()

        elif self.radio_decode.isChecked() and event in self.decoders_list:
            self.params['last_decoder'] = event
            if coders.is_key(event) == coders.KEY_DECIMAL:
                self.show_key_spin()
            elif coders.is_key(event) == coders.KEY_TEXT:
                self.show_key_field()

        elif event in self.hashes_list:
            self.params['last_hash'] = event

    def get_md(self, string, algorithm):
        """Process text string through selected
        by drop-down menu hash-function
        and return function return.

        Args:
            string: Text string for hashing.
            algorithm: Text string defines hash-algorithm.

        Returns:
            Text string - hash-function hexdigest.

        """
        hash_obj = hashlib.new(algorithm, string.encode('utf-8'))
        try:
            sig = signature(hash_obj.hexdigest).parameters
        except ValueError:
            sig = ()
        if len(sig) == 0:
            return hash_obj.hexdigest()
        else:
            return hash_obj.hexdigest(1024)

    def encode(self, string, algorithm, key=None):
        """Process text through selected by drop-down menu encoding function

        Args:
            string: Text string for encryption.
            algorithm: Text string defines encryption algorithm.
            key: Text string or integer - key for text encryption.

        Returns:
            Text string - encryption result.

        """
        error, text = coders.encode(string, algorithm, key)
        if error:
            self.show_error(error['title'], error['text'])
        return text

    def decode(self, string, algorithm, key=None):
        """Process encrypted text through selected
        by drop-down menu decoding function

        Args:
            string: Encrypted text string for decryption.
            algorithm: Text string defines encryption algorithm.
            key: Text string or integer - key for text decryption.

        Returns:
            Text string - decryption result.

        """
        error, text = coders.decode(string, algorithm, key)
        if error:
            self.show_error(error['title'], error['text'])
        return text

    def convert(self):
        """Convert button callback,
        select method by checked radiobutton and drop-down menu
        than process text through selected function.

        Gets text string and place processed text from/to text_field

        """
        self.hide_error()
        key_type = coders.is_key(self.coding_selector.currentText())
        key = None
        if key_type == coders.KEY_DECIMAL:
            key = self.key_spin.value()
        elif key_type == coders.KEY_TEXT:
            key = self.key_field.text()

        if self.radio_encode.isChecked():
            text = self.encode(self.text_field.toPlainText(),
                               self.coding_selector.currentText(),
                               key)

        elif self.radio_decode.isChecked():
            text = self.decode(self.text_field.toPlainText(),
                               self.coding_selector.currentText(),
                               key)

        elif self.radio_hash.isChecked():
            text = self.get_md(self.text_field.toPlainText(),
                               self.coding_selector.currentText())

        else:
            raise ZeroDivisionError('Oh shi~')

        self.text_field.setPlainText(text)

    def show_key_spin(self):
        """Show numeric key field"""
        self.hile_key_field()
        self.key_label.show()
        self.key_spin.show()

    def hile_key_spin(self):
        """Hide numeric key field"""
        self.key_label.hide()
        self.key_spin.hide()

    def show_key_field(self):
        """Show text key field"""
        self.hile_key_spin()
        self.key_label.show()
        self.key_field.show()

    def hile_key_field(self):
        """Hide text key field"""
        self.key_label.hide()
        self.key_field.hide()

    def set_drop_down_coders(self):
        """Fill drop-down menu with coders methods"""
        index = 0
        if 'last_coder' in self.params:
            index = self.coders_list.index(self.params['last_coder'])
        self.coding_selector.clear()
        self.coding_selector.addItems(self.coders_list)
        self.coding_selector.setCurrentIndex(index)

    def set_drop_down_decoders(self):
        """Fill drop-down menu with decoders methods"""
        index = 0
        if 'last_decoder' in self.params:
            index = self.decoders_list.index(self.params['last_decoder'])
        self.coding_selector.clear()
        self.coding_selector.addItems(self.decoders_list)
        self.coding_selector.setCurrentIndex(index)

    def set_drop_down_hashes(self):
        """Fill drop-down menu with hash algorithms"""
        index = 0
        if 'last_hash' in self.params:
            index = self.hashes_list.index(self.params['last_hash'])
        self.coding_selector.clear()
        self.coding_selector.addItems(self.hashes_list)
        self.coding_selector.setCurrentIndex(index)

    def hide_error(self):
        """Hide error text label"""
        self.error_label.hide()

    def show_error(self, error_title, error_text):
        """Show error text label with some data about error in tooltip"""
        self.error_label.setText(error_title)
        self.error_label.setToolTip(error_text)
        self.error_label.setStyleSheet("color: red")
        self.error_label.show()


def main():
    """Create and open main window"""
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
