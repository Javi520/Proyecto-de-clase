#!/usr/bin/env python3


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Atk
from view import View

# Búsqueda
class View1(View):
    @classmethod
    def main(cls):
        Gtk.main()

    @classmethod
    def main_quit(cls, w, e):
        Gtk.main_quit()    

    def show_all(self):
        self.win.show_all()
    
    def hide_all(self):
        self.win.hide()

    def update_view(self, **kwargs):
        for name, value in kwargs.items():
            if name == 's_name':
                self.search_name.set_text(value)
            elif name == 's_surname':
                self.search_surname.set_text(value)
            elif name == 'search_name_is_ok':
                self._update_entry_is_valid(self.search_name, value)
            elif name == 'search_enabled':
                self.search.set_sensitive(value)
            elif name == 'stop_visibility':
                self.stop.set_no_show_all(not value)
                self.stop.set_visible(value)
            elif name == 'stop_sensitivity':
                self.stop.set_sensitive(value)
            else:
                raise TypeError(f"update_view() got an unexpected keyword argument '{name}'")

    def build_view(self, name = "", surname = ""):
        label_s_name = Gtk.Label(label= ("Search by name:"), xalign=0)
        self.search_name = Gtk.Entry(text= "", name= 'Search_name')
        self.search_name.set_placeholder_text(("p.a. {}").format(name))
        self.search_name.get_accessible().add_relationship(Atk.RelationType.LABELLED_BY,
                                                          label_s_name.get_accessible())
        box_name = Gtk.Box(orientation= Gtk.Orientation.HORIZONTAL)
        box_name.pack_start(label_s_name, True, True, 0)
        box_name.pack_start(self.search_name, False, False, 10)

        label_s_surname = Gtk.Label(label= ("Search by surname:"), xalign=0)
        self.search_surname = Gtk.Entry(text= "", name= 'Search_surname')
        self.search_surname.set_placeholder_text(("p.a. {}").format(surname))
        self.search_surname.get_accessible().add_relationship(Atk.RelationType.LABELLED_BY,
                                                           label_s_surname.get_accessible())
        box_surname = Gtk.Box(orientation= Gtk.Orientation.HORIZONTAL)
        box_surname.pack_start(label_s_surname, True, True, 0)
        box_surname.pack_start(self.search_surname, False, False, 10)
        
        self.search = Gtk.Button(label= ("Search"))
        self.search.set_sensitive(False)

        self.stop = Gtk.Button(label= ("Stop"))
        self.stop.set_no_show_all(True)
        self.stop.set_sensitive(False)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin=10)
        vbox.pack_start(box_name, False, False, 0)
        vbox.pack_start(box_surname, False, False, 0)
        vbox.pack_start(self.search, False, False, 0)
        vbox.pack_start(self.stop, True, True, 0)
        
        self.win = Gtk.Window(title= ("UDC Watcher"))
        self.win.set_default_size(1,1) # Trick, Is there a cleaner way?
        self.win.add(vbox)

    def connect_delete_event(self, fun):
        self.win.connect('delete-event', fun)

    def connect_search_name_changed(self, fun):
        self.search_name.connect('changed', fun)

    def connect_search_surname_changed(self, fun):
        self.search_surname.connect('changed', fun)

    def connect_search_clicked(self, fun):
        self.search.connect('clicked', fun)
    
    def connect_stop_clicked(self, fun):
        self.stop.connect('clicked', fun)