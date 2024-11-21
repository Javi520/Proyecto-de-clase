from random import Random
from dogtail.tree import *
from dogtail.procedural import *

class Utilities:
    def launchProgram(path: str, app_name: str):
    ########## Launching program ###########
        pid = run('python3 '+ path, appName= 'watcher.py')
    ########## Searching program ###########
        program:Node = root.application(app_name)
        print("Debug:")
        print("\tpid: " + int.__str__(pid))
        print("\tprogram: ", program)
        return pid, program

    def nSpaces() -> int:
        rand = Random()
        rand.seed()
        space = ""
        for i in range(0, rand.randint(1, 5)):
            space = space.__add__(" ")
        return space