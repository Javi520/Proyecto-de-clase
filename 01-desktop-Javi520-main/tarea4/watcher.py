#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from view1 import View1
from view2 import View2
from view3 import View3
from w_model import WatcherData
from controller1 import Controller1
from controller2 import Controller2
from controller3 import Controller3

if __name__=="__main__":
    model = WatcherData()

    controller1 = Controller1()
    controller1.set_model(model)
    model.insertListener(controller1)
    controller1.set_view(View1())

    controller2 = Controller2()
    controller2.set_model(model)
    model.insertListener(controller2)
    controller2.set_view(View2())

    controller3 = Controller3()
    controller3.set_model(model)
    model.insertListener(controller3)
    controller3.set_view(View3())
    
    controller1.main()
