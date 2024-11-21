#!/usr/bin/env python3

import datetime

from requests.models import HTTPError, ConnectionError
from exceptions import UserNotFound
from listener import Listener


class Controller1(Listener):
    def set_model(self, model):
        self.model = model

    def set_view(self, view):
        self.view = view
        view.build_view(name= "Rosa", surname= "Melano")

        view.connect_delete_event(self.view.main_quit)
        view.connect_search_name_changed(self.on_search_name_changed)
        view.connect_search_surname_changed(self.on_search_surname_changed)
        view.connect_search_clicked(self.on_search_clicked)

    def main(self):
        self.view.show_all()
        self.view.main()
        
    def on_search_name_changed(self, entry):
        name = entry.get_text()
        self.model.search_name = name
        print("Setting model.search_name as "+name)
        print("Is name empty? "+(lambda var: "True" if (var=="") else "False")(name))
        self._update_view()
        
    def on_search_surname_changed(self, entry):
        surname = entry.get_text()
        self.model.search_surname = surname
        print("Setting model.search_surname as "+surname)
        print("Is surname empty? "+(lambda var: "True" if (var=="") else "False")(surname))
        self._update_view()

    def _update_view(self, **kwargs):
        if(self.model.is_valid()):
            data_is_valid = True
        else:
            data_is_valid = False
        self.view.update_view(search_enabled= data_is_valid,
                              **kwargs)

    def update_view2(self, **kwargs):
        self.view.update_view(s_name= self.model.search_name, s_surname= self.model.search_surname, **kwargs)
    
    def search_action(self):
        print("Search_event on controller 1")
        self.view.hide_all()

    def track_action(self):
        print("Track_event on controller 1")

    def on_search_clicked(self, w):
        try:
            self.model.search()
            self.update_view2()
        except ConnectionError:
            self.view.show_error("There was an error connecting with the database, sorry, check your connection")
        except HTTPError as err:
            self.view.show_error("There was an internal error related to database, sorry for the inconvenience")
        except UserNotFound as err:
            self.view.show_error("User has not been found on database. Please check ""name"" and ""surname"" try again. Also check the capital letters, " +
            "users in DB seems to: capital letter and lowercase letters")

    def _parse_date(self, s):
        try:
            return datetime.datetime.strptime(s, "%x")
        except ValueError:
            return None