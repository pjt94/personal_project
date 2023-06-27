# :coding: utf-8

import os
import sys
import json
from PyQt4 import QtGui
from PyQt4.QtGui import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QListWidget, QListWidgetItem, QFormLayout

class AutoRVPackageView(QMainWindow):
    def __init__(self):
        super(AutoRVPackageView, self).__init__()

        self.setWindowTitle("auto_rv_package")
        self.setMinimumSize(300, 150)
        current_directory = os.getcwd()
        self.log_folder_path = os.path.join(current_directory, '.log')
        self.json_file_path = os.path.join(self.log_folder_path, 'select_package_list.json')

        self.package_inputs = {}
        self.setup_ui()

    def setup_ui(self):
        path_button = QPushButton("set path:", self)
        self.path_input = QLineEdit(self)

        label_list = ['package_name', 'author', 'organization', 'contact', 'version', 'requires', 'system', 'hidden', 'optional', 'rv', 'url', 'package_file', 'shortcut', 'event', 'description']
        
        package_form_layout = QFormLayout()  # Use QFormLayout instead of QVBoxLayout

        for label in label_list:
            package_label = QLabel("%s:"%label, self)
            package_input = QLineEdit(self)

            self.package_inputs[label] = package_input

            package_form_layout.addRow(package_label, package_input)

        self.accept_button = QPushButton("accept", self)
        cancel_button = QPushButton("cancel", self)

        select_package_button = QPushButton("select package", self)
        reset_button = QPushButton("reset", self)

        self.select_package_list_widget = QListWidget(self)

        path_button.clicked.connect(self.set_path_button)  
        
        cancel_button.clicked.connect(self.close)
        select_package_button.clicked.connect(self.get_select_package_list)
        reset_button.clicked.connect(self.reset)

        path_layout = QHBoxLayout()
        path_layout.addWidget(path_button)
        path_layout.addWidget(self.path_input)

        extra_button_layout = QHBoxLayout()
        extra_button_layout.addWidget(select_package_button, 3)
        extra_button_layout.addWidget(reset_button, 1)

        package_list_layout = QVBoxLayout()
        package_list_layout.addWidget(self.select_package_list_widget)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.accept_button)
        button_layout.addWidget(cancel_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(path_layout)
        main_layout.addLayout(package_form_layout)
        main_layout.addLayout(extra_button_layout)
        main_layout.addLayout(package_list_layout)
        main_layout.addLayout(button_layout)
        
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
    
    def set_path_button(self):
        path = self._getfolder_list()
        self.path_input.setText(path[0])

    def remove_package_item(self, item, label):
        row = self.select_package_list_widget.row(item)
        list_item = self.select_package_list_widget.item(row)
        self.select_package_list_widget.takeItem(row)

        item_text = label.label.text()
        item_text_list = self._read_json(self.json_file_path)
        item_text_list.remove(item_text)
        self._make_json_file(item_text_list)

    def reset(self):
        self.select_package_list_widget.clear()
        self._clear_json(self.json_file_path)

    def _get_file_list(self):
        file_dialog = QtGui.QFileDialog()
        file_dialog.setFileMode(QtGui.QFileDialog.ExistingFiles)

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            selected_files = [str(file_path) for file_path in selected_files]
            return selected_files
        
        return []

    def _getfolder_list(self):
        folder_dialog = QtGui.QFileDialog()
        folder_dialog.setFileMode(QtGui.QFileDialog.Directory)

        if folder_dialog.exec_():
            selected_folders = folder_dialog.selectedFiles()
            selected_folders = [str(folder_path) for folder_path in selected_folders]
            return selected_folders

        return []

    def _make_log_folder(self):
        log_folder_path = self.log_folder_path
        
        if not os.path.exists(log_folder_path):
            os.mkdir(log_folder_path)

    def _make_json_file(self, select_package_list):
        path = self.json_file_path

        with open(path, 'w') as file:
            json.dump(select_package_list, file)

    def get_select_package_list(self):
        self._make_log_folder()
        select_package_list = self._get_file_list()
        self._make_json_file(select_package_list)
        

        self.select_package_list_widget.clear()
        item_text_list = self._read_json(self.json_file_path)

        for item_text in item_text_list:
            list_item_widget = ListItemWidget(item_text)

            remove_button = list_item_widget.remove_button
            
            list_item = QListWidgetItem()
            list_item.setSizeHint(list_item_widget.sizeHint())
            self.select_package_list_widget.addItem(list_item)
            self.select_package_list_widget.setItemWidget(list_item, list_item_widget)

            remove_button.clicked.connect(lambda _, item = list_item, label = list_item_widget: self.remove_package_item(item, label))
    
    def _clear_json(self, path):
        data = ''
        if os.path.exists(path):
            with open(path, 'w') as file:
                json.dump(data, file)

    def _read_json(self, path):
        with open(path, 'r') as file:
            data = json.load(file)
        if data:
            return data
        else:
            return ""

class ListItemWidget(QWidget):
    def __init__(self, text):
        super(ListItemWidget, self).__init__()

        self.text = text

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.label = QLabel(text)
        self.remove_button = QPushButton("-")
        self.remove_button.setFixedSize(20, 20)

        layout.addWidget(self.label)
        layout.addWidget(self.remove_button)

        self.setLayout(layout)