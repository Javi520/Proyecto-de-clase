#!/usr/bin/env python3

import datetime
from exceptions import NoMoreAccesses
from listener import Listener
import w_model
from w_model import WatcherData, PersonData, Accesses


class Controller2(Listener):
    def set_model(self, model):
        self.model = model

    def set_view(self, view):
        self.view = view
        view.build_view(name = "Unknown",
            surname = "Unknown",
            email = "Unknown",
            tel = "xxx-xxx-xxx",
            is_v = False)

        view.connect_delete_event(self.view.main_quit)
        view.connect_since_changed(self.on_since_changed)
        view.connect_until_changed(self.on_until_changed)
        view.connect_track_clicked(self.on_track_clicked)
        view.connect_prev_event(self.on_prev_clicked)
        view.connect_s_hour_changed(self.on_s_hour_changed)
        view.connect_s_minute_changed(self.on_s_minute_changed)
        view.connect_u_hour_changed(self.on_u_hour_changed)
        view.connect_u_minute_changed(self.on_u_minute_changed)
        view.connect_sig_event(self.on_sig_clicked)

    def main(self):
        self.view.show_all()
        self.view.main()
        
    def on_since_changed(self, entry):
        since_striped = entry.get_date()
        self.model.since = since_striped
        self._update_view()
        
    def on_until_changed(self, entry):
        until_striped = entry.get_date()
        self.model.until = until_striped
        self._update_view()

    def on_s_hour_changed(self, entry):
        value = entry.get_text().strip()
        value = int(value)
        aux = self.model.s_time
        if(value < 0 or value > 23):
            self.view.update_view(s_hour_changed=False)
            self.model.s_time = None, aux[1]
        else:
            self.model.s_time = value, aux[1]
            self.view.update_view(s_hour_changed=True)
        self._update_view()

    def on_s_minute_changed(self, entry):
        value = entry.get_text().strip()
        value = int(value)
        aux = self.model.s_time
        if(value < 0 or value > 59):
            self.view.update_view(s_minute_changed=False)
            self.model.s_time = aux[0], None
        else:
            self.model.s_time = aux[0], value
            self.view.update_view(s_minute_changed=True)
        self._update_view()

    def on_u_hour_changed(self, entry):
        value = entry.get_text().strip()
        value = int(value)
        aux = self.model.u_time
        if(value < 0 or value > 23):
            self.view.update_view(u_hour_changed=False)
            self.model.u_time = None, aux[1]
        else:
            self.model.u_time = value, aux[1]
            self.view.update_view(u_hour_changed=True)
        self._update_view()

    def on_u_minute_changed(self, entry):
        value = entry.get_text().strip()
        value = int(value)
        aux = self.model.u_time
        if(value < 0 or value > 59):
            self.view.update_view(u_minute_changed=False)
            self.model.u_time = aux[0], None
        else:
            self.model.u_time = aux[0], value
            self.view.update_view(u_minute_changed=True)
        self._update_view()

    def _update_view(self, **kwargs):
        since_date_is_valid, until_date_is_valid = self.model.valid_dates()
        track_is_enabled = self.model.valid_time() & since_date_is_valid & until_date_is_valid
        self.view.update_view(since_date_is_ok= since_date_is_valid, until_date_is_ok=until_date_is_valid, track_sensitive=track_is_enabled, **kwargs)
        
    def on_track_clicked(self, w):
        #self.view.update_view(profile_update= ["Rosa", "Melano", "colacao@colacao.com", "Hola", True, []])
        #try:
            self.model.track()
        #except Exception as err:
        #    print(err)

    def on_prev_clicked(self, w):
        try:
            self.model.dataUser.accesses.prev()
            self.view.update_view(sig_sensitive=True)
            accesses, (more, less) = self.model.dataUser.accesses.getAccesses()
            self.view.update_view(access_update= Accesses.accessesToList(accesses), decr_page= "")
            if(less):
                raise NoMoreAccesses
            if(more):
                self.view.update_view(sig_sensitive=False)
        except NoMoreAccesses:
            self.view.update_view(prev_sensitive=False)

    def on_sig_clicked(self, w):
        try:
            self.model.dataUser.accesses.next()
            accesses, (more, less) = self.model.dataUser.accesses.getAccesses()
            self.view.update_view(access_update= Accesses.accessesToList(accesses)
                , prev_sensitive=True
                , incr_page= "")
            if(more):
                self.view.update_view(sig_sensitive=False)
        except NoMoreAccesses:
            self.view.update_view(sig_sensitive=False)


    def _parse_date(self, s):
        try:
            return datetime.datetime.strptime(s, "%x")
        except ValueError:
            return None
    
    ## listeners events

    def track_action(self):
        self.view.hide_all()

    def search_action(self):
        print("Search_event on controller 2")
        self.view.show_all()
        accesses, (more, less) = self.model.dataUser.accesses.getAccesses()
        #load profile
        self.view.update_view(profile_update= [
                self.model.dataUser.name,
                self.model.dataUser.surname,
                self.model.dataUser.email,
                self.model.dataUser.phone,
                self.model.dataUser.is_vaccinated,
                Accesses.accessesToList(accesses)
            ], prev_sensitive= False, sig_sensitive= not more)
        #self.model.dataUser.accesses.next()
        #self.view.get_time()
        self._update_view()
        #["Rosa", "Melano", "colacao@colacao.com", "Hola", True])