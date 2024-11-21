#!/usr/bin/env python3

import abc
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Atk

class View(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def show_all(self):
        """Method documentation"""
        
    def hide_all(self):
        """Method documentation"""

    def update_view(self, **kwargs):
        """Method documentation"""

    def show_ok(self, text):
        """
            Dialog showing that everything is ok

            Attributes
            ----------
            text : any
                The text that will be displayed in the dialog
        """
        dialog = Gtk.MessageDialog(parent= self.win,
                                   message_type= Gtk.MessageType.INFO,
                                   buttons= Gtk.ButtonsType.OK,
                                   text= text)
        dialog.run()
        dialog.destroy()

    def show_error(self, text):
        """
            Dialog showing that an error has ocurred

            Attributes
            ----------
            text : any
                The text that will be displayed in the dialog
        """
        dialog = Gtk.MessageDialog(parent= self.win,
                                   message_type= Gtk.MessageType.ERROR,
                                   buttons= Gtk.ButtonsType.CLOSE,
                                   text= text)
        dialog.run()
        dialog.destroy()

    def show_options(self, text, fun):
        """
            Dialog showing options regarding to a I/O operation

            Attributes
            ----------
            text: any
                The text that will be displayed in the dialog
            fun: function
                The function to run when user choose to stop the operation
        """
        dialog = Gtk.MessageDialog(parent= self.win,
                                   message_type= Gtk.MessageType.OK,
                                   buttons= Gtk.ButtonsType.CLOSE,
                                   text= text)
        dialog.run()
        dialog.destroy()