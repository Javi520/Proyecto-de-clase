#!/usr/bin/env python3


import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Atk
from view import View

class View3(View):
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
            if name == 'prev_page':
                self
            elif name == 'sig_page':
                self
            elif name == 'incr_page':
                self.incrLabel()
            elif name == 'decr_page':
                self.decrLabel()
            elif name == 'prev_enabled':
                self.prev_button.set_sensitive(True)
            elif name == 'sig_enabled':
                self.sig_button.set_sensitive(True)
            elif name == 'prev_disabled':
                self.prev_button.set_sensitive(False)
            elif name == 'sig_disabled':
                self.sig_button.set_sensitive(False)
            elif name == 'access_update':
                self._update_accesses(value)
            else:
                raise TypeError(f"update_view() got an unexpected keyword argument '{name}'")

    def _update_accesses(self, data_list):
        print("Updating user's accesses")
        self.list_store.clear()
        for data in data_list:
            self.list_store.append(list(data))

    def build_view(self):

        #OUTTER BOX
        self.vbox_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        #INNER BOX 1
        self.vbox_inner1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.vbox_outer.pack_start(self.vbox_inner1, True, True, 0)

        # Creating the ListStore model
        self.list_store = Gtk.ListStore(str, str, str, str, bool, int)


        # creating the treeview, and adding the columns
        self.treeview = Gtk.TreeView(self.list_store)
        for i, column_title in enumerate(["Name", "Surname", "Email", "Phone", "Is vaccinated?", "Facility id"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)
        self.vbox_inner1.pack_start(self.treeview, True, True, 0)

    #INNER BOX 2
        self.hbox_inner2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.vbox_outer.pack_start(self.hbox_inner2, True, True, 0)
        
        #prev_button PREVIOUS
        #self.prev_button = Gtk.Button(label="<-")
        self.prev_button = Gtk.Button(label="Reset")
        #self.prev_button.connect("clicked", self.on_prev_button_clicked)
        self.hbox_inner2.pack_start(self.prev_button, False, False, 0)
        
        #LABEL nº
        self.current_page = 1
        self.page_label = Gtk.Label(self.current_page)
        self.hbox_inner2.pack_start(self.page_label, True, True, 0)
        
        #sig_button NEXT
        self.sig_button = Gtk.Button(label="Sig")
        #self.sig_button.connect("clicked", self.on_sig_button_clicked)
        self.hbox_inner2.pack_start(self.sig_button, False, False, 0)

        self.win = Gtk.Window(title= ("Tracking: UDC Watcher"))
        self.win.set_default_size(1,1) # Trick, Is there a cleaner way?
        self.win.add(self.vbox_outer)

    def incrLabel(self):
        self.current_page += 1
        self.page_label.set_text(int.__str__(self.current_page))

    def decrLabel(self):
        self.current_page  = 1
        self.page_label.set_text(int.__str__(self.current_page))

    def connect_delete_event(self, fun):
        self.win.connect('delete-event', fun)

    def connect_prev_event(self, fun):
        self.prev_button.connect('clicked', fun)
    
    def connect_sig_event(self, fun):
        self.sig_button.connect('clicked', fun)

