#!/usr/bin/python3
import os
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
blog = BLog('tests_results_1.txt')

blog.logn_("Begging tests of View1 fields with incorrect name and surname")
blog.logn_("")

########################################
###### Search with empty fields ########
########################################

pid, watcher = Utilities.launchProgram(this_path, 'watcher.py')

try:
    Search_sensitivity = watcher.child(name= 'Search', roleName= 'push button').sensitive
    assert (Search_sensitivity == False)
    print("Search with empty fields -> OK")
    blog.logn("Search with empty fields -> OK")
except AssertionError:
    print("Search with empty fields -> ERROR")
    blog.logn("Search with empty fields -> ERROR", positivity= False)
    #print("Error: Search button should be non sensitive")
except SearchError:
    print("Error while searching node")
    blog.logn("Search with empty fields -> ERROR", positivity= False)
except Exception as err:
    print("Another error", err)
    blog.logn("Search with empty fields -> ERROR", positivity= False)

os.kill(pid, 1)


########################################
#### Search only one field (name) ######
########################################

pid, watcher = Utilities.launchProgram(this_path, 'watcher.py')

try:
    watcher.childLabelled('Search by name:').typeText('Hola')
    Search_sensitivity = watcher.child(name= 'Search', roleName= 'push button').sensitive
    assert (Search_sensitivity == False)
    print("Search only one field (name) -> OK")
    blog.logn("Search only one field (name) -> OK")
except AssertionError:
    print("Search only one field (name) -> ERROR")
    blog.logn("Search only one field (name) -> ERROR", positivity= False)
    #print("Error: Search button should be non sensitive")
except SearchError:
    print("Error while searching node")
    blog.logn("Search only one field (name) -> ERROR", positivity= False)
except Exception as err:
    print("Another error", err)
    blog.logn("Search only one field (name) -> ERROR", positivity= False)

os.kill(pid, 1)


########################################
#### Search only one field (surname) ###
########################################

pid, watcher = Utilities.launchProgram(this_path, 'watcher.py')

try:
    watcher.childLabelled('Search by surname:').typeText('Hola')
    Search_sensitivity = watcher.child(name= 'Search', roleName= 'push button').sensitive
    assert (Search_sensitivity == False)
    print("Search only one field (surname) -> OK")
    blog.logn("Search only one field (surname) -> OK")
except AssertionError:
    print("Search only one field (surname) -> ERROR")
    blog.logn("Search only one field (surname) -> ERROR", positivity= False)
    #print("Error: Search button should be non sensitive")
except SearchError:
    print("Error while searching node")
    blog.logn("Search only one field (surname) -> ERROR", positivity= False)
except Exception as err:
    print("Another error", err)
    blog.logn("Search only one field (surname) -> ERROR", positivity= False)

os.kill(pid, 1)


########################################
#### Search with non-empty fields ######
########################################

pid, watcher = Utilities.launchProgram(this_path, 'watcher.py')

try:
    watcher.childLabelled('Search by name:').typeText('Hola')
    watcher.childLabelled('Search by surname:').typeText('Hola')
    Search_sensitivity = watcher.child(name= 'Search', roleName= 'push button').sensitive
    assert (Search_sensitivity == True)
    print("Search with non-empty fields -> OK")
    blog.logn("Search with non-empty fields -> OK")
except AssertionError:
    print("Search with non-empty fields -> ERROR")
    blog.logn("Search with non-empty fields -> ERROR", positivity= False)
    #print("Error: Search button should be sensitive")
except SearchError:
    print("Error while searching node")
    blog.logn("Search with non-empty fields -> ERROR", positivity= False)
except Exception as err:
    print("Another error", err)
    blog.logn("Search with non-empty fields -> ERROR", positivity= False)

os.kill(pid, 1)


########################################
##### Wrong field[s] Search test #######
########################################

pid, watcher = Utilities.launchProgram(this_path, 'watcher.py')

try:
    watcher.childLabelled('Search by name:').typeText('Hola')
    watcher.childLabelled('Search by surname:').typeText('Hola')
    watcher.child(name= 'Search', roleName= 'push button').click()
    #TODO: error message could happen also if there is a problem with DB's connection
    error = watcher.child(roleName= 'alert')
    error.child(roleName= 'push button').click()
    assert (True)
    print("Wrong field's Search test -> OK")
    blog.logn("Wrong field's Search test -> OK")
except AssertionError:
    print("Wrong field's Search test -> ERROR")
    blog.logn("Wrong field's Search test -> ERROR", positivity= False)
    #print("Error: Search button should be sensitive")
except SearchError:
    print("Error while searching node")
    blog.logn("Wrong field's Search test -> ERROR", positivity= False)
except Exception as err:
    print("Another error", err)
    blog.logn("Wrong field's Search test -> ERROR", positivity= False)

os.kill(pid, 1)


blog.logn_()
blog.logn_("Begging tests of View1 fields with correct name and surname")
blog.logn_()

#Test objectives
    #Case sensitiveness (since it's a DB thing, to use case letters, we don't care)

    #Space in between?

    #Space at the beginning of a field
        #name field
        #surname field
        #both

    #Space at the end of a field
        #name field
        #surname field
        #both

    #Both cases together?

########################################
#### Periferical whitespaces removal ###
########################################

# pid, watcher = Utilities.launchProgram(this_path, 'watcher.py')

# try:
#     watcher.childLabelled('Search by name:').typeText('Hola')
#     watcher.childLabelled('Search by surname:').typeText('Hola')
#     Search_sensitivity = watcher.child(name= 'Search', roleName= 'push button').sensitive
#     assert (Search_sensitivity == True)
#     print("Search with non-empty fields -> OK")
#     blog.logn("Search with non-empty fields -> OK")
# except AssertionError:
#     print("Search with non-empty fields -> ERROR")
#     blog.logn("Search with non-empty fields -> ERROR", positivity= False)
#     #print("Error: Search button should be sensitive")
# except SearchError:
#     print("Error while searching node")
#     blog.logn("Search with non-empty fields -> ERROR", positivity= False)
# except Exception as err:
#     print("Another error", err)
#     blog.logn("Search with non-empty fields -> ERROR", positivity= False)

# os.kill(pid, 1)


########################################
##### Correct fields Search test #######
########################################

pid, watcher = Utilities.launchProgram(this_path, 'watcher.py')

try:
    watcher.childLabelled('Search by name:').typeText('Jorge')
    watcher.childLabelled('Search by surname:').typeText('Jimenez')
    watcher.child(name= 'Search', roleName= 'push button').click()
    error = watcher.child(roleName= 'alert')
    error.child(roleName= 'push button').click()
    print("Correct fields Search test -> ERROR")
    blog.logn("Correct fields Search test -> ERROR", positivity= False)
    #Error: no error should have happened, unless DB's connectivity related
    assert (False)
except AssertionError:
    print("Can't happen this")
except SearchError:
    print("Error while searching node")
    print("Correct fields Search test -> OK")
    blog.logn("Correct fields Search test -> OK")
except Exception as err:
    print("Another error", err)
    blog.logn("Correct fields Search test -> ERROR", positivity= False)

os.kill(pid, 1)


# We test the removal of the whitespace in name fields
########################################
#### Semi-correct name Search test #####
########################################

pid, watcher = Utilities.launchProgram(this_path, 'watcher.py')

try:
    watcher.childLabelled('Search by name:').typeText(Utilities.nSpaces() + 'Jorge' + Utilities.nSpaces())
    watcher.childLabelled('Search by surname:').typeText('Jimenez')
    watcher.child(name= 'Search', roleName= 'push button').click()
    error = watcher.child(roleName= 'alert')
    error.child(roleName= 'push button').click()
    print("Semi-correct name Search test -> ERROR")
    blog.logn("Semi-correct name Search test -> ERROR", positivity= False)
    #TODO: no error should have happened, unless DB's connectivity related
    assert (False)
except AssertionError:
    print("Can't happen this")
except SearchError:
    print("Error while searching node")
    print("Semi-correct name Search test -> OK")
    blog.logn("Semi-correct name Search test -> OK")
except Exception as err:
    print("Another error", err)
    blog.logn("Semi-correct name Search test -> ERROR", positivity= False)

os.kill(pid, 1)


# We test the removal of the whitespace in name fields
########################################
## Semi-correct surname Search test ####
########################################

pid, watcher = Utilities.launchProgram(this_path, 'watcher.py')

try:
    watcher.childLabelled('Search by name:').typeText('Jorge')
    watcher.childLabelled('Search by surname:').typeText(Utilities.nSpaces() + 'Jimenez' + Utilities.nSpaces())
    watcher.child(name= 'Search', roleName= 'push button').click()
    error = watcher.child(roleName= 'alert')
    error.child(roleName= 'push button').click()
    print("Semi-correct surname Search test -> ERROR")
    blog.logn("Semi-correct surname Search test -> ERROR", positivity= False)
    #TODO: no error should have happened, unless DB's connectivity related
    assert (False)
except AssertionError:
    print("Can't happen this")
except SearchError:
    print("Error while searching node")
    print("Semi-correct surname Search test -> OK")
    blog.logn("Semi-correct surname Search test -> OK")
except Exception as err:
    print("Another error", err)
    blog.logn("Semi-correct surname Search test -> ERROR", positivity= False)

os.kill(pid, 1)


############ closing tests #############

blog.bake()