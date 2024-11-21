#!/usr/bin/env python3

import datetime
from exceptions import NoBeforeAccesses, NoMoreAccesses
from listener import Listener
import w_model

class Controller3(Listener):
    def set_model(self, model):
        self.model = model
    
    def set_view(self, view):
        self.view = view; 
        self.view.build_view()


        view.connect_delete_event(self.view.main_quit)
        view.connect_prev_event(self.prev_event)
        view.connect_sig_event(self.sig_event)

    ## listener's actions

    def search_action(self):
        print("Search_event on controller 3")
        #this controller doesnt care about this event

    def track_action(self):
        print("Track_event on controller 3")
        self.view.show_all()
        self._update_view()
    
    def prev_event(self, w):
        try:
            self.view.update_view(sig_enabled=None
                , access_update= self.model.track_reset()
                , decr_page = "")
        except NoBeforeAccesses:#):
            self.view.update_view(prev_disabled=None)

    def sig_event(self, w):
        try:
            self.view.update_view(access_update= self.model.track_next(), incr_page = "")
            if(not self.model.track_hasNext()):
                self.view.update_view(sig_disabled=None)
        except NoMoreAccesses:#):
            self.view.update_view(sig_disabled=None)

    def _update_view(self, **kwargs):
        #since_date_is_valid, until_date_is_valid = self.model.valid_dates()
        #self.view.update_view(since_date_is_ok= since_date_is_valid, until_date_is_ok=until_date_is_valid, **kwargs)
        self.view.update_view(access_update= self.model.track_next())

    def main(self):
        self.view.show_all()
        self.view.main()