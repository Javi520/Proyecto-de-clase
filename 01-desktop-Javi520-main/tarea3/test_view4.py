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
from gi import require_version
require_version('Atspi', '2.0')
from gi.repository import Atspi

old_path = '/home/javi/ipm/tarea2/Program/watcher.py'
this_path = '/home/javi/ipm/tarea4/watcher.py'

def step_la_interface_sigue_respondiendo(app: Atspi.Object) -> None:
    # ELiminamos el timeout de arrancar la app
    Atspi.set_timeout(800, -1)
    if app.get_name() != "watcher.py":
        raise AssertionError

def localizador_programa(name: str) -> Atspi.Object:
    aux = Atspi.get_desktop(0)
    for a in aux:
        if(a.name == name):
            return a
    return None

######### Creating a log file ##########
blog = BLog('tests_results_4.txt')

blog.logn_("Beggining tests of IO concurrency")
blog.logn_("")


blog.logn_("")
blog.logn_("#### Concurrency test ####")
blog.logn_("")

########################################
##### Task 2 No concurrency at all #####
########################################

blog.logn_("")
blog.logn_("#### Task 2 Non Concurrency test ####")
blog.logn_("")

pid, watcher = Utilities.launchProgram(old_path, 'watcher.py')
programa_atspi = localizador_programa('watcher.py')

try:
    # somes serious stuff
    watcher.childLabelled('Search by name:').typeText('Jorge')
    watcher.childLabelled('Search by surname:').typeText('Jimenez')
    watcher.child(name= 'Search', roleName= 'push button').click()
    step_la_interface_sigue_respondiendo(programa_atspi)
    print("Interface is still acepting user input while searching")
    blog.logn("Interface is still acepting user input while searching -> ERROR", positivity= True)
except AssertionError:
    print("Interface is not acepting user input while searching -> OK by AssertionError")
    blog.logn("Interface is not acepting user input while searching -> OK", positivity= True)
except SearchError:
    print("Error while searching node")
    print("Search Error while testing concurrency -> ERROR")
    blog.logn("SearchError while testing concurrency -> ERROR", positivity= False)
except Exception as err:
    print("Another error", err)
    blog.logn("Another error while testing concurrency -> ERROR", positivity= False)


os.kill(pid, 1)


########################################
#### Task 4 Concurrency implemented ####
########################################

blog.logn_("")
blog.logn_("#### Task 4 Concurrency test ####")
blog.logn_("")

pid, watcher = Utilities.launchProgram(this_path, 'watcher.py')
programa_atspi = localizador_programa('watcher.py')

try:
    # somes serious stuff
    watcher.childLabelled('Search by name:').typeText('Jorge')
    watcher.childLabelled('Search by surname:').typeText('Jimenez')
    watcher.child(name= 'Search', roleName= 'push button').click()
    step_la_interface_sigue_respondiendo(programa_atspi)
    print("Interface is still acepting user input while searching")
    blog.logn("Interface is still acepting user input while searching -> OK", positivity= True)
except AssertionError:
    print("Interface is still acepting user input while searching -> ERROR by AssertionError")
    blog.logn("Interface is still acepting user input while searching -> ERROR", positivity= False)
except SearchError:
    print("Error while searching node")
    print("Interface is still acepting user input while searching -> ERROR")
    blog.logn("Interface is still acepting user input while searching -> ERROR", positivity= False)
except Exception as err:
    print("Another error", err)
    blog.logn("Interface is still acepting user input while searching -> ERROR", positivity= False)


os.kill(pid, 1)



############ closing tests #############

blog.bake()