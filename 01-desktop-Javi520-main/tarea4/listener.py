#!/usr/bin/env python3

from re import match
from typing import Match


class Listener:
    s_u_event = 0
    track_event = 1

    def __init(self):
        pass

    def search_action(self):
        print("search_action")

    def track_action(self):
        print("track_action")

    def action(self, event):
        if(event == self.s_u_event):
            self.search_action()
        elif(event == self.track_event):
            self.track_action()