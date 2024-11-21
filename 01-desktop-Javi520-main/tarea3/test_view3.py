#!/usr/bin/python3
import os
from typing import Union
from b_log_utils import BLog
from utilities import Utilities
from random import Random
from dogtail.config import config
from dogtail.tree import *
config.logDebugToFile = False
from dogtail.procedural import *
from dogtail.tc import TCNode, TCBool

this_path = '/home/javi/ipm/tarea2/Program/watcher.py'

######### Creating a log file ##########
blog = BLog('tests_results_3.txt')

blog.logn_("Begging tests of View3")
blog.logn_("")

def launchAndReach(path: str, app_name: str):
    pid: int
    watcher: Node
    #we launch our program first
    pid, watcher = Utilities.launchProgram(path, app_name)
    try:
        watcher.childLabelled('Search by name:').typeText('Jorge')
        watcher.childLabelled('Search by surname:').typeText('Jimenez')
        watcher.child(name= 'Search', roleName= 'push button').click()
        watcher.child(name='Track', roleName= 'push button').click()
        return pid, watcher
    except SearchError:
        blog.logn_("Fatal error: Program could not be launched")
        blog.bake()
        exit()

def aux(label_: str, info, watcher_: Node, boolean: bool = False):
    try:
        if(boolean):
            assert (watcher_.childLabelled(label_).isChecked == info)
        else:
            watcher_.child(name= info)
            assert True
        blog.logn(label_ + " info -> OK")
        print(label_ + " info -> OK")
    except AssertionError:
        #Error: label_ is not the one expected
        blog.logn(label_ + " info -> ERROR", positivity= False)
        print(label_ + " info -> ERROR")
    except SearchError:
        print("Error while searching node")
        blog.logn(label_ + " info -> ERROR", positivity= False)
        print(label_ + " info -> ERROR")
    except Exception as err:
        print("Another error", err)
        blog.logn(label_ + " info -> ERROR", positivity= False)


blog.logn_("")
blog.logn_("#### Init & Reset button provoques same results ####")
blog.logn_("")

########################################
### Init & Reset button same results ###
########################################

pid, watcher = launchAndReach(this_path, 'watcher.py')

try:
    name = watcher.child('Name').text
    surname = watcher.child('Surname').text
    email = watcher.child('Email').text
    phone = watcher.child('Phone').text
    is_vac = watcher.child('Is vaccinated?').text
    fac_id = watcher.child('Facility id').text

    watcher.child("Sig", roleName= "push button").click()
    watcher.child("Reset", roleName= "push button").click()
    assert (
        name == watcher.child('Name').text and
        surname == watcher.child('Surname').text and
        email == watcher.child('Email').text and
        phone == watcher.child('Phone').text and
        is_vac == watcher.child('Is vaccinated?').text and
        fac_id == watcher.child('Facility id').text
    )
    print("Init & Reset button provoques same results -> OK")
    blog.logn("Init & Reset button provoques same results -> OK", positivity= True)
except AssertionError:
    print("Init & Reset button provoques same results -> ERROR")
    blog.logn("Init & Reset button provoques same results -> ERROR", positivity= False)
except SearchError:
    print("Error while searching node")
    print("Init & Reset button provoques same results -> ERROR")
    blog.logn("Init & Reset button provoques same results -> ERROR", positivity= False)
except Exception as err:
    print("Another error", err)
    blog.logn("Init & Reset button provoques same results -> ERROR", positivity= False)


os.kill(pid, 1)


blog.logn_("")
blog.logn_("#### Current page reset ####")
blog.logn_("")

########################################
########## Current page reset ##########
########################################

pid, watcher = launchAndReach(this_path, 'watcher.py')

try:
    watcher.child("1")
    watcher.child("Sig", roleName= "push button").click()
    watcher.child("Sig", roleName= "push button").click()
    watcher.child("Reset", roleName= "push button").click()
    watcher.child("1")
    print("Current page reset -> OK")
    blog.logn("Current page reset -> OK", positivity= True)
except SearchError:
    print("Error while searching node")
    print("Current page reset -> ERROR")
    blog.logn("Current page reset -> ERROR", positivity= False)
except Exception as err:
    print("Another error", err)
    blog.logn("Current page reset -> ERROR", positivity= False)


os.kill(pid, 1)


blog.logn_("")
blog.logn_("#### Sig page sensitivity on last accesses ####")
blog.logn_("")

########################################
# Sig page sensitivity on last accesses#
########################################

pid, watcher = launchAndReach(this_path, 'watcher.py')

try:

    for i in range(28):
        watcher.child("Sig", roleName= "push button").click()
    assert watcher.child("Sig", roleName= "push button").sensitive == False
    print("Sig page sensitivity on last accesses -> OK")
    blog.logn("Sig page sensitivity on last accesses -> OK", positivity= True)
except AssertionError:
    print("Sig page sensitivity on last accesses -> ERROR")
    blog.logn("Sig page sensitivity on last accesses -> ERROR", positivity= False)
except SearchError:
    print("Error while searching node")
    print("Sig page sensitivity on last accesses -> ERROR")
    blog.logn("Sig page sensitivity on last accesses -> ERROR", positivity= False)
except Exception as err:
    print("Another error", err)
    blog.logn("Sig page sensitivity on last accesses -> ERROR", positivity= False)


os.kill(pid, 1)



############ closing tests #############

blog.bake()