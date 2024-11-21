#!/usr/bin/env python3


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Atk
from view import View

# User profile
class View2(View):
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
            if name == 'profile_update':
                self.label_name.set_text(value[0])
                self.label_surname.set_text(value[1])
                self.label_email.set_text(value[2])
                self.label_tel.set_text(value[3])
                if(value[4]):
                    self.check_is_v.set_active(True)
                self._update_accesses(value[5])
                print(value[5])
            elif name == 'since_date_is_ok':
                self._update_entry_is_valid(self.since, value)
            elif name == 'until_date_is_ok':
                self._update_entry_is_valid(self.until, value)
            elif name == 'access_update':
                self._update_accesses(value)
            elif name == 'dates_valid':
                self._update_entry_is_valid(self.since, value)
                self._update_entry_is_valid(self.until, value)
            elif name == 'sig_sensitive':
                print("received update petition of type sig_sensitive")
                self.next_button.set_sensitive(value);
            elif name == 'prev_sensitive':
                print("received update petition of type prev_sensitive")
                self.prev_button.set_sensitive(value);
            elif name == 's_hour_changed':
                print("received update petition of type s_hour_changed")
                if(not value):
                    self.s_hour.get_style_context().add_class('error')
                else:
                    self.s_hour.get_style_context().remove_class('error')
            elif name == 's_minute_changed':
                print("received update petition of type s_minute_changed")
                if(not value):
                    self.s_minute.get_style_context().add_class('error')
                else:
                    self.s_minute.get_style_context().remove_class('error')
            elif name == 'u_hour_changed':
                print("received update petition of type u_hour_changed")
                if(not value):
                    self.u_hour.get_style_context().add_class('error')
                else:
                    self.u_hour.get_style_context().remove_class('error')
            elif name == 'u_minute_changed':
                print("received update petition of type u_minute_changed")
                if(not value):
                    self.u_minute.get_style_context().add_class('error')
                else:
                    self.u_minute.get_style_context().remove_class('error')
            elif name == 'incr_page':
                self.incrLabel()
            elif name == 'decr_page':
                self.decrLabel()
            elif name == 'track_sensitive':
                self.track.set_sensitive(value)
            else:
                raise TypeError(f"update_view() got an unexpected keyword argument '{name}'")
    
    def _update_accesses(self, data_list):
        print("Updating user's accesses")
        self.list_store.clear()
        for data in data_list:
            self.list_store.append(list(data))

    def _update_entry_is_valid(self, entry, is_valid):
        if is_valid:
            entry.get_style_context().remove_class('error')
        else:
            entry.get_style_context().add_class('error')
    
    def get_time(self):
        return (self.s_hour.get_value()
                , self.s_minute.get_value()
                , self.u_hour.get_value()
                , self.u_minute.get_value()
                , self.since.get_date()
                , self.until.get_date())

    def build_view(self, name = "Rosa", surname = "Melano", email = "alocao@colacao.com", tel = 123456789, is_v = True):
        lab_name = Gtk.Label(label= ("Name:"), xalign=0)
        self.label_name = Gtk.Label(label= (name), xalign=0)

        box_name = Gtk.Box(orientation= Gtk.Orientation.HORIZONTAL)
        box_name.pack_start(lab_name, False, True, 0)
        box_name.pack_start(self.label_name, False, False, 10)

        lab_surname = Gtk.Label(label= ("Surname:"), xalign=0)
        self.label_surname = Gtk.Label(label= (surname), xalign=0)

        box_surname = Gtk.Box(orientation= Gtk.Orientation.HORIZONTAL)
        box_surname.pack_start(lab_surname, False, True, 0)
        box_surname.pack_start(self.label_surname, False, False, 10)
        
        lab_email = Gtk.Label(label= ("Email:"), xalign=0)
        self.label_email = Gtk.Label(label= (email), xalign=0)

        box_email = Gtk.Box(orientation= Gtk.Orientation.HORIZONTAL)
        box_email.pack_start(lab_email, False, True, 0)
        box_email.pack_start(self.label_email, False, False, 10)
        
        lab_tel = Gtk.Label(label= ("Telephone:"), xalign=0)
        self.label_tel = Gtk.Label(label= (tel), xalign=0)

        box_tel = Gtk.Box(orientation= Gtk.Orientation.HORIZONTAL)
        box_tel.pack_start(lab_tel, False, True, 0)
        box_tel.pack_start(self.label_tel, False, False, 10)
        
        lab_is_v = Gtk.Label(label= ("Is vaccinated?"), xalign=0)
        self.check_is_v = Gtk.CheckButton()
        self.check_is_v.set_sensitive(False)

        self.check_is_v.get_accessible().add_relationship(Atk.RelationType.LABELLED_BY,
                                                          lab_is_v.get_accessible())

        box_is_v = Gtk.Box(orientation= Gtk.Orientation.HORIZONTAL)
        box_is_v.pack_start(lab_is_v, False, True, 0)
        box_is_v.pack_start(self.check_is_v, False, False, 10)

        # COVID

        lab_since = Gtk.Label(label= ("Since (optional)"), xalign=0)
        self.since = Gtk.Calendar()
        self.since.get_accessible().add_relationship(Atk.RelationType.LABELLED_BY,
                                                          lab_since.get_accessible())
        self.since.select_day(20)
        self.since.select_month(10, 1995)
        label_s_hour = Gtk.Label(label= ("since_hours"), name= "u_hours")
        self.s_hour = Gtk.SpinButton()
        self.s_hour.get_accessible().add_relationship(Atk.RelationType.LABELLED_BY,
                                                          label_s_hour.get_accessible())
        self.s_hour.set_adjustment(Gtk.Adjustment(value=0, lower=0, upper=23, step_incr=1, page_incr=1, ))
        self.s_hour.set_wrap(True)
        self.s_hour.set_digits(0)

        self.s_dot = Gtk.Label(label= (":"))

        label_s_minute = Gtk.Label(label= ("since_minutes"), name= "u_minutes")
        self.s_minute = Gtk.SpinButton()
        self.s_minute.get_accessible().add_relationship(Atk.RelationType.LABELLED_BY,
                                                          label_s_minute.get_accessible())
        self.s_minute.set_adjustment(Gtk.Adjustment(value=0, lower=0, upper=59, step_incr=1, page_incr=1, ))
        self.s_minute.set_wrap(True)
        self.s_minute.set_digits(0)
        #self.since = Gtk.Entry(xalign=0)
        #self.since.set_placeholder_text("Since (start)")
        box_su = Gtk.Box(orientation= Gtk.Orientation.HORIZONTAL)
        box_su2 = Gtk.Box(orientation= Gtk.Orientation.HORIZONTAL)
        box_su.pack_start(lab_since, False, False, 10)
        box_su.pack_start(self.since, False, False, 10)
        box_su2.pack_start(self.s_hour, True, False, 10)
        box_su2.pack_start(self.s_dot, True, False, 10)
        box_su2.pack_start(self.s_minute, True, False, 10)

        lab_until = Gtk.Label(label= ("Until (optional)"), xalign=0)
        self.until = Gtk.Calendar()
        self.until.get_accessible().add_relationship(Atk.RelationType.LABELLED_BY,
                                                          lab_until.get_accessible())
        self.until.select_day(20)
        self.until.select_month(10, 2995)
        label_u_hour = Gtk.Label(label= ("until_hours"), name= "u_hours")
        self.u_hour = Gtk.SpinButton()
        self.u_hour.get_accessible().add_relationship(Atk.RelationType.LABELLED_BY,
                                                          label_u_hour.get_accessible())
        self.u_hour.set_adjustment(Gtk.Adjustment(value=0, lower=0, upper=23, step_incr=1, page_incr=1, ))
        self.u_hour.set_wrap(True)
        self.u_hour.set_digits(0)

        self.u_dot = Gtk.Label(label= (":"))

        label_u_minute = Gtk.Label(label= ("until_minutes"), name= "u_minutes")
        self.u_minute = Gtk.SpinButton()
        self.u_minute.get_accessible().add_relationship(Atk.RelationType.LABELLED_BY,
                                                          label_u_minute.get_accessible())
        self.u_minute.set_adjustment(Gtk.Adjustment(value=0, lower=0, upper=59, step_incr=1, page_incr=1, ))
        self.u_minute.set_wrap(True)
        self.u_minute.set_digits(0)
        #self.until = Gtk.Entry(xalign=0)
        #self.until.set_placeholder_text("Until (start)")
        box_su.pack_start(lab_until, False, False, 10)
        box_su.pack_start(self.until, False, False, 10)
        box_su2.pack_start(self.u_hour, True, False, 10)
        box_su2.pack_start(self.u_dot, True, False, 10)
        box_su2.pack_start(self.u_minute, True, False, 10)

        self.track = Gtk.Button(name= "Track", label="Track", xalign=0)
        box_su.pack_start(self.track, False, False, 10)

        self.list_store = Gtk.ListStore(str, str, str, str, str, int)

        self.treeview = Gtk.TreeView(self.list_store)
        
        self.button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        
        #Button1 PREVIOUS
        self.prev_button = Gtk.Button(label="Prev")
        #self.prev_button.connect("clicked", self.on_prev_button_clicked)
        self.button_box.pack_start(self.prev_button, True, True, 0)
        #LABEL nº
        self.current_page = 1
        self.page_label = Gtk.Label(self.current_page)
        self.button_box.pack_start(self.page_label, True, True, 0)
        
        #BUTTON2 NEXT
        self.next_button = Gtk.Button(label="Sig")
        #self.next_button.connect("clicked", self.on_next_button_clicked)
        self.button_box.pack_start(self.next_button, True, True, 0)

        for i, column_title in enumerate(
            ["Timestamp", "Temperature(ºC)", "Type", "Facility Name", "Facility Address", "Fac.: Id"]
        ):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin=10)
        vbox.pack_start(box_name, False, False, 0)
        vbox.pack_start(box_surname, False, False, 0)
        vbox.pack_start(box_email, False, False, 0)
        vbox.pack_start(box_tel, False, False, 0)
        vbox.pack_start(box_is_v, False, False, 0)
        vbox.pack_start(box_su, False, False, 0)
        vbox.pack_start(box_su2, False, False, 0)
        vbox.pack_start(self.treeview, True, True, 0)
        #vbox.pack_start(self.next_button, False, False, 0)
        #vbox.pack_start(self.page_label, False, False, 0)
        #vbox.pack_start(self.prev_button, False, False, 0)
        vbox.pack_start(self.button_box, True, True, 0)

        self.win = Gtk.Window(title= ("Profile: UDC Watcher"))
        self.win.set_default_size(1,1) # Trick, Is there a cleaner way?
        self.win.add(vbox)

    def incrLabel(self):
        self.current_page += 1
        self.page_label.set_text(int.__str__(self.current_page))

    def decrLabel(self):
        self.current_page  = max(1, (self.current_page - 1))
        self.page_label.set_text(int.__str__(self.current_page))

    def connect_delete_event(self, fun):
        self.win.connect('delete-event', fun)

    ## Widget event's listeners

    def connect_s_hour_changed(self, fun):
        self.s_hour.connect('changed', fun)

    def connect_s_minute_changed(self, fun):
        self.s_minute.connect('changed', fun)

    def connect_u_hour_changed(self, fun):
        self.u_hour.connect('changed', fun)
    
    def connect_u_minute_changed(self, fun):
        self.u_minute.connect('changed', fun)

    def connect_since_changed(self, fun):
        self.since.connect('day-selected', fun)

    def connect_until_changed(self, fun):
        self.until.connect('day-selected', fun)

    def connect_track_clicked(self, fun):
        self.track.connect('clicked', fun)
    
    def connect_prev_event(self, fun):
        self.prev_button.connect('clicked', fun)
    
    def connect_sig_event(self, fun):
        self.next_button.connect('clicked', fun)