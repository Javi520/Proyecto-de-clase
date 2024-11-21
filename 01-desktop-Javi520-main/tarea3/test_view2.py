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
blog = BLog('tests_results_2.txt')

blog.logn_("Begging tests of View2")
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
blog.logn_("#### Correct fields displayed ####")
blog.logn_("")

########################################
#### Correct fields Display test #######
########################################

pid, watcher = launchAndReach(this_path, 'watcher.py')

aux("Name:", "Jorge", watcher)
aux("Surname:", "Jimenez", watcher)
aux("Email:", "jorge.jimenez@example.com", watcher)
aux("Telephone:", "984-126-887", watcher)
aux("Is vaccinated?", True, watcher, True)

#os.kill(pid, 1)


blog.logn_("")
blog.logn_("#### Prev & Sig sensitivity & Page content with first accesses ####")
blog.logn_("")

###############################################
### Buttons sensitivity with first accesses ###
###############################################

#pid, watcher = launchAndReach(this_path, 'watcher.py')

try:
    assert watcher.child('Prev', roleName="push button").sensitive == False
    print("Prev button sensitivity with first accesses -> OK")
    blog.logn("Prev button sensitivity with first accesses -> OK", positivity= True)
    #TODO: no error should have happened, unless DB's connectivity related
except AssertionError:
    print("Prev button sensitivity with first accesses -> ERROR")
    blog.logn("Prev button sensitivity with first accesses -> ERROR", positivity= False)
except SearchError:
    print("Error while searching node")
    print("Prev button sensitivity with first accesses -> ERROR")
    blog.logn("Prev button sensitivity with first accesses -> ERROR", positivity= False)
except Exception as err:
    print("Another error", err)
    blog.logn("Prev button sensitivity with first accesses -> ERROR", positivity= False)

try:
    watcher.child('1', roleName="label")
    print("Page content equals 1 with first accesses -> OK")
    blog.logn("Page content equals 1 with first accesses -> OK", positivity= True)
    #TODO: no error should have happened, unless DB's connectivity related
except SearchError:
    print("Error while searching node")
    print("Page content equals 1 with first accesses -> ERROR")
    blog.logn("Page content equals 1 with first accesses -> ERROR", positivity= False)
except Exception as err:
    print("Another error", err)
    blog.logn("Page content equals 1 with first accesses -> ERROR", positivity= False)

try:
    assert watcher.child('Sig', roleName="push button").sensitive == True
    print("Sig button sensitivity with first accesses -> OK")
    blog.logn("Sig button sensitivity with first accesses -> OK", positivity= True)
    #TODO: no error should have happened, unless DB's connectivity related
except AssertionError:
    print("Sig button sensitivity with first accesses -> ERROR")
    blog.logn("Sig button sensitivity with first accesses -> ERROR", positivity= False)
except SearchError:
    print("Error while searching node")
    print("Sig button sensitivity with first accesses -> ERROR")
    blog.logn("Sig button sensitivity with first accesses -> ERROR", positivity= False)
except Exception as err:
    print("Another error", err)
    blog.logn("Sig button sensitivity with first accesses -> ERROR", positivity= False)


os.kill(pid, 1)


blog.logn_("")
blog.logn_("#### Prev & Sig sensitivity & Page content with seconds accesses ####")
blog.logn_("")

###############################################
## Buttons sensitivity with second accesses ###
###############################################

pid, watcher = launchAndReach(this_path, 'watcher.py')

try:
    watcher.child('Sig', roleName= "push button").click()
    assert watcher.child('Prev', roleName="push button").sensitive == True
    print("Prev button sensitivity with second accesses -> OK")
    blog.logn("Prev button sensitivity with second accesses -> OK", positivity= True)
    #TODO: no error should have happened, unless DB's connectivity related
except AssertionError:
    print("Prev button sensitivity with second accesses -> ERROR")
    blog.logn("Prev button sensitivity with second accesses -> ERROR", positivity= False)
except SearchError:
    print("Error while searching node")
    print("Prev button sensitivity with second accesses -> ERROR")
    blog.logn("Prev button sensitivity with second accesses -> ERROR", positivity= False)
except Exception as err:
    print("Another error", err)
    blog.logn("Prev button sensitivity with second accesses -> ERROR", positivity= False)

try:
    watcher.child('2', roleName="label")
    print("Page content equals 2 with second accesses -> OK")
    blog.logn("Page content equals 2 with second accesses -> OK", positivity= True)
    #TODO: no error should have happened, unless DB's connectivity related
except SearchError:
    print("Error while searching node")
    print("Page content equals 2 with second accesses -> ERROR")
    blog.logn("Page content equals 2 with second accesses -> ERROR", positivity= False)
except Exception as err:
    print("Another error", err)
    blog.logn("Page content equals 2 with second accesses -> ERROR", positivity= False)

try:
    assert watcher.child('Sig', roleName="push button").sensitive == True
    print("Sig button sensitivity with second accesses -> OK")
    blog.logn("Sig button sensitivity with second accesses -> OK", positivity= True)
    #TODO: no error should have happened, unless DB's connectivity related
except AssertionError:
    print("Sig button sensitivity with second accesses -> ERROR")
    blog.logn("Sig button sensitivity with second accesses -> ERROR", positivity= False)
except SearchError:
    print("Error while searching node")
    print("Sig button sensitivity with second accesses -> ERROR")
    blog.logn("Sig button sensitivity with second accesses -> ERROR", positivity= False)
except Exception as err:
    print("Another error", err)
    blog.logn("Sig button sensitivity with second accesses -> ERROR", positivity= False)


os.kill(pid, 1)


blog.logn_("")
blog.logn_("#### Prev & Sig sensitivity & Page content with last accesses ####")
blog.logn_("")

###############################################
## Buttons sensitivity with last accesses ###
###############################################

pid, watcher = launchAndReach(this_path, 'watcher.py')

watcher.child('Sig', roleName= "push button").click()
watcher.child('Sig', roleName= "push button").click()
watcher.child('Sig', roleName= "push button").click()
watcher.child('Sig', roleName= "push button").click()

try:
    assert watcher.child('Sig', roleName="push button").sensitive == False
    print("Sig button sensitivity with last accesses -> OK")
    blog.logn("Sig button sensitivity with last accesses -> OK", positivity= True)
    #TODO: no error should have happened, unless DB's connectivity related
except AssertionError:
    print("Sig button sensitivity with last accesses -> ERROR")
    blog.logn("Sig button sensitivity with last accesses -> ERROR", positivity= False)
except SearchError:
    print("Error while searching node")
    print("Sig button sensitivity with last accesses -> ERROR")
    blog.logn("Sig button sensitivity with last accesses -> ERROR", positivity= False)
except Exception as err:
    print("Another error", err)
    blog.logn("Sig button sensitivity with last accesses -> ERROR", positivity= False)


os.kill(pid, 1)


blog.logn_("")
blog.logn_("#### Prev sensitivity and Page count when going to start again ####")
blog.logn_("")

###############################################
## Prev sensitivity when going to start again #
###############################################

pid, watcher = launchAndReach(this_path, 'watcher.py')

watcher.child('Sig', roleName= "push button").click()

watcher.child('Prev', roleName= "push button").click()

try:
    assert watcher.child('Prev', roleName="push button").sensitive == False
    print("Prev sensitivity when going to start again -> OK")
    blog.logn("Prev sensitivity when going to start again -> OK", positivity= True)
    #TODO: no error should have happened, unless DB's connectivity related
except AssertionError:
    print("Prev sensitivity when going to start again -> ERROR")
    blog.logn("Prev sensitivity when going to start again -> ERROR", positivity= False)
except SearchError:
    print("Error while searching node")
    print("Prev sensitivity when going to start again -> ERROR")
    blog.logn("Prev sensitivity when going to start again -> ERROR", positivity= False)
except Exception as err:
    print("Another error", err)
    blog.logn("Prev sensitivity when going to start again -> ERROR", positivity= False)

try:
    watcher.child('1', roleName="label")
    print("Page count when going to start again -> OK")
    blog.logn("Page count when going to start again -> OK", positivity= True)
    #TODO: no error should have happened, unless DB's connectivity related
except SearchError:
    print("Error while searching node")
    print("Page count when going to start again -> ERROR")
    blog.logn("Page count when going to start again -> ERROR", positivity= False)
except Exception as err:
    print("Another error", err)
    blog.logn("Page count when going to start again -> ERROR", positivity= False)


os.kill(pid, 1)


pid, watcher = launchAndReach(this_path, 'watcher.py')

try:
    watcher.child("Track", roleName="push button").click()
    watcher.child("Track", roleName="push button")
    print("View 3 start on Track event -> ERROR", positivity= False)
    blog.logn("View 3 start on Track event -> ERROR", positivity= False)
except SearchError:
    print("View 3 start on Track event -> OK")
    blog.logn("View 3 start on Track event -> OK")
except Exception as err:
    print("Another error", err)
    blog.logn("Page count when going to start again -> ERROR", positivity= False)    


os.kill(pid, 1)



############ closing tests #############

blog.bake()