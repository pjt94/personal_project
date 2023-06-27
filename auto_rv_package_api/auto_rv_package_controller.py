# :coding: utf-8

import sys
from PyQt4.QtGui import QApplication
from auto_rv_package_model import AutoRVPackage
from auto_rv_package_view import AutoRVPackageView

class AutoRVPackageController():
    def __init__(self):  
        app = QApplication(sys.argv)
        self.arv = AutoRVPackageView()
        self.ar = AutoRVPackage()
        self.json_file_path = self.arv.json_file_path
        self.arv.accept_button.clicked.connect(self.accept_button)
        self.arv.show()
        sys.exit(app.exec_())

    def accept_button(self):
        select_package_list = self.arv._read_json(self.json_file_path)
        self.set_text()

        if select_package_list:
            self.ar.zip_package(select_package_list)
        else:
            print("Please select the list to package.")

    def set_text(self):
        self.ar._set_path = str(self.arv.path_input.text())
        self.ar._package_name = str(self.arv.package_inputs["package_name"].text())
        self.ar._author = str(self.arv.package_inputs["author"].text())
        self.ar._organization = str(self.arv.package_inputs["organization"].text())
        self.ar._contact = str(self.arv.package_inputs["contact"].text())
        self.ar._version = str(self.arv.package_inputs["version"].text())
        self.ar._requires = str(self.arv.package_inputs["requires"].text())
        self.ar._system = str(self.arv.package_inputs["system"].text())
        self.ar._hidden = str(self.arv.package_inputs["hidden"].text())
        self.ar._optional = str(self.arv.package_inputs["optional"].text())
        self.ar._rv = str(self.arv.package_inputs["rv"].text())
        self.ar._url = str(self.arv.package_inputs["url"].text())
        self.ar._package_file = str(self.arv.package_inputs["package_file"].text())
        self.ar._shortcut = str(self.arv.package_inputs["shortcut"].text())
        self.ar._event = str(self.arv.package_inputs["event"].text())
        self.ar._description = str(self.arv.package_inputs["description"].text())

def main():
    arc = AutoRVPackageController()

if __name__ == "__main__":
    main()