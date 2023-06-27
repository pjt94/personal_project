# :coding: utf-8

import os
import subprocess
import json
import shutil
from PyQt4 import QtGui

class AutoRVPackage():

    def __init__(self):
        self._set_path = None
        self._package_name = None
        self._author = None
        self._organization = None
        self._contact = None
        self._url = None
        self._version = None
        self._requires = None
        self._system = None
        self._hidden = None
        self._optional = None
        self._rv = None
        self._package_file = None
        self._shortcut = None
        self._event = None
        self._description = None

    @property
    def set_path(self):
        return self._set_path
    
    @set_path.setter
    def set_path(self, value):
        self._set_path = value

    @property
    def package_name(self):
        return self._package_name

    @package_name.setter
    def package_name(self, value):
        self._package_name = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        self._author = value

    @property
    def organization(self):
        return self._organization

    @organization.setter
    def organization(self, value):
        self._organization = value

    @property
    def contact(self):
        return self._contact

    @contact.setter
    def contact(self, value):
        self._contact = value

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        self._version = value

    @property
    def requires(self):
        return self._requires

    @requires.setter
    def requires(self, value):
        self._requires = value

    @property
    def system(self):
        return self._system

    @system.setter
    def system(self, value):
        self._system = value

    @property
    def hidden(self):
        return self._hidden

    @hidden.setter
    def hidden(self, value):
        self._hidden = value

    @property
    def optional(self):
        return self._optional

    @optional.setter
    def optional(self, value):
        self._optional = value

    @property
    def rv(self):
        return self._rv

    @rv.setter
    def rv(self, value):
        self._rv = value

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def package_file(self):
        return self._package_file

    @package_file.setter
    def package_file(self, value):
        self._package_file = value

    @property
    def shortcut(self):
        return self._shortcut

    @shortcut.setter
    def shortcut(self, value):
        self._shortcut = value

    @property
    def event(self):
        return self._event

    @event.setter
    def event(self, value):
        self._event = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    def zip_package(self, package_list):
        zip_name = self._get_zip_name()
        set_path = self._make_set_path()
        zip_path = set_path + "/" + zip_name
        print(zip_path)
        package_txt_file = self._make_text_file(set_path)
        py_list = []

        for py_path in package_list:
            py_name = py_path.split("/")[-1]
            copy_file = set_path + "/" + py_name
            py_list.append(copy_file)
            self._copy_file(py_path, set_path)

        if os.path.exists(set_path):
            zip_command = ['zip', '-r', zip_path, '.']
            subprocess.Popen(zip_command, cwd= set_path).wait()

    def _make_package_dict(self):
        package_name = self._filter_info(self._package_name)
        author = self._filter_info(self._author)
        organization = self._filter_info(self._organization)
        contact = self._filter_info(self._contact)
        version = self._filter_info(self._version)
        requires = self._filter_info(self._requires)
        system = self._system
        hidden = self._hidden
        optional = self._filter_info(self._optional)
        rv = self._filter_info(self._rv)
        url = self._filter_info(self._url)
        package_file = self._filter_info(self._package_file)
        menu = self._get_menu(package_name)
        shortcut = self._filter_info(self._shortcut)
        event = self._filter_info(self._event)
        description = self._get_description()

        package_dict = {
            "package" : package_name,
            "author" : author,
            "organization" : organization,
            "contact" : contact,
            "version" : version,
            "requires" : requires,
            "system" : system,
            "hidden" : hidden,
            "optional" : optional,
            "rv" : rv,
            "url" : url,
            "modes" : {"  - file" : package_file,
            "    menu" : menu,
            "    shortcut" : shortcut,
            "    event" : event,
            "    load" : "immediate"},
            "description" : description
        }

        return package_dict

    def _make_text_file(self, path):
        package_dict = self._make_package_dict()
        text_path = '%s'%path + '/' + 'PACKAGE'
        key_list = ["package", "author", "organization", "contact", "version", "requires", "system", "hidden", "optional", "rv", "url", "modes", "description"]
        sub_key_list = ["  - file", "    menu", "    shortcut", "    event", "    load"]

        with open(text_path, "w") as file:
            for key, value in sorted(package_dict.items(), key = lambda x: key_list.index(x[0])):
                if not isinstance(value, dict) and key != 'description':
                    file.write(key + ": " + value + "\n")

                elif isinstance(value, dict):
                    file.write("\n")
                    file.write(key + ":\n")
                    for sub_key, sub_value in sorted(value.items(), key = lambda y: sub_key_list.index(y[0])):
                        file.write(" " + sub_key + ": " + sub_value + "\n")

                else:
                    file.write("\n")
                    file.write(key + ": " + value + "\n")
        
        return text_path

    def _make_set_path(self):
        set_path = self._set_path
        package_name = self._package_name
        zip_name = self._get_zip_name()
        forlder_name = zip_name[:-6]
        new_forlder = set_path + "/" + forlder_name

        if not forlder_name in os.listdir(set_path):
            os.mkdir(new_forlder)
            return new_forlder
        else:
            print("The forlder is already existed.")
            return new_forlder

    def _copy_file(self, source, destination):
        source_file = source
        destination_file = destination

        shutil.copy(source_file, destination_file)

    def _get_menu(self, name):
        package_name = "".join(name.split(" "))
        menu = "Tools" + "/" + package_name
        return menu

    def _get_description(self):
        description_text = self._description
        description = "|\n" + "    <p>\n" + "    %s\n"%description_text + "    <p>"
        return description

    def _filter_info(self, info):
        if info == "" or '' or None:
            return "\'""\'"
        else:
            return info

    def _get_zip_name(self):
        package_name = self._package_name
        converted_name = "_".join(package_name.lower().split())
        version = self._version
        zip_name = converted_name + '-' + version + '.rvpkg'
        return zip_name