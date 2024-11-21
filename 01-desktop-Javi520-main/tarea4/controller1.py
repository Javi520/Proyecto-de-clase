#!/usr/bin/env python3

import datetime

from requests.models import HTTPError, ConnectionError
from exceptions import UserNotFound, IgnoreSearch
#from listener import Listener
from controller import Controller
import threading
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib


class Controller1(Controller):
    is_searching = False
    reject_search = False

    def set_view(self, view):
        self.view = view
        view.build_view(name= "Rosa", surname= "Melano")

        view.connect_delete_event(self.view.main_quit)
        view.connect_search_name_changed(self.on_search_name_changed)
        view.connect_search_surname_changed(self.on_search_surname_changed)
        view.connect_search_clicked(self.on_search_clicked)
        view.connect_stop_clicked(self.on_stop_clicked)

    def on_stop_clicked(self, w):
        self.reject_search = True

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

    def _search(self):
        try:
            self.is_searching = False
            self.reject_search = False
            self.view.update_view(stop_visibility= True, stop_sensitivity= True)
            self.is_searching = True
            self.model.search()
            error = None
        except ConnectionError as err:
            error = err
        except HTTPError as err:
            error = err
        except UserNotFound as err:
            error = err
        except IgnoreSearch as err:
            error = err
        except Exception as err:
            error = err
        finally:
            GLib.idle_add(lambda: self.aux(error))

    def aux(self, error: Exception):
        self.is_searching = False
        print(error)
        if(self.reject_search):
            self.view.update_view(stop_visibility= False)
            return
        if(type(error) == ConnectionError):
            self.view.update_view(stop_visibility= False)
            self.view.show_error("There was an error connecting with the database, sorry, check your connection")
            return
        if(type(error) == HTTPError):
            self.view.update_view(stop_visibility= False)
            self.view.show_error("There was an internal error related to database, sorry for the inconvenience")
            return
        if(type(error) == UserNotFound):
            self.view.update_view(stop_visibility= False)
            self.view.show_error("User has not been found on database. Please check ""name"" and ""surname"" try again. Also check the capital letters, " +
            "users in DB seems to: capital letter and lowercase letters")
            return
        if(type(error) == IgnoreSearch):
            self.view.update_view(stop_visibility= False)
            return
        if(error is None):
            self.model.succesfull_search()
            return
            #gg wp
        else:
            print(error)
            self.view.update_view(stop_visibility= False)
            self.view.show_error("Unkown error has ocurred")


    def on_search_clicked(self, w):
        try:
            if not self.is_searching:
                threading.Thread(target= self._search, daemon= True).start()
                self.update_view2()
            else:
                self.view.show_error("Another search in progress")
        except Exception as err:
            print(err)
            self.view.update_view(stop_visibility= False)
            self.view.show_error("Unkown error has ocurred")

    def _parse_date(self, s):
        try:
            return datetime.datetime.strptime(s, "%x")
        except ValueError:
            return None