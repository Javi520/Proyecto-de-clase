#!/usr/bin/env python3.9
from __future__ import annotations

import re

from ipm import e2e


program = "../tarea2/Program/watcher.py"
from pathlib import Path
import random
import subprocess
import time
from typing import Any, Iterator, NamedTuple, Optional, Union

#-------------------------------------------------------------------------------
# Primer test Formato entrada
#-------------------------------------------------------------------------------

# GIVEN he lanzado la aplicación
path = ""
process, app = e2e.run(program)
## Compruebo que todo fue bien
if app is None:
    process and process.kill()
    assert False, f"La aplicación {path} no aparece en el escritorio"

    
# THEN veo el texto "Has pulsado 0 veces"

do, shows = e2e.perform_on(app)
do()
assert shows(role= "label", text= "Has pulsado 0 veces")


# TERMINO EL TEST DEJANDO TODO COMO ESTABA
process and process.kill()

#-------------------------------------------------------------------------------
# Segundo test
#-------------------------------------------------------------------------------

# GIVEN he lanzado la aplicación
process, app = e2e.run(program)
## Compruebo que todo fue bien
if app is None:
    process and process.kill()
    assert False, f"La aplicación {path} no aparece en el escritorio"

   
# WHEN pulso el botón 'Contar'

do, shows = e2e.perform_on(app)
do('click', role= 'push button', name= 'Contar')


# THEN veo el texto "Has pulsado 1 vez"

assert shows(role= "label", text= "Has pulsado 1 vez")


# TERMINO EL TEST DEJANDO TODO COMO ESTABA
process and process.kill()


#-------------------------------------------------------------------------------
# Tercer test
#-------------------------------------------------------------------------------

# GIVEN he lanzado la aplicación
process, app = e2e.run(program)
## Compruebo que todo fue bien
if app is None:
    process and process.kill()
    assert False, f"La aplicación {path} no aparece en el escritorio"


# WHEN pulso el botón 'Contar' cuatro veces
do, _shows = e2e.perform_on(app, role= 'push button', name= 'Contar')
do('click')
do('click')
do('click')
do('click')


# THEN veo el texto "Has pulsado 4 veces"
_do, shows = e2e.perform_on(app, role= 'label', text= re.compile('^Has pulsado.*'))
assert shows(text= "Has pulsado 4 veces")

_do, shows = e2e.perform_on_each((app,), role= 'label')
assert any(shows(text= "Has pulsado 4 veces")), "Nigún label muestra 'Has pulsado 4 veces'"


# TERMINO EL TEST DEJANDO TODO COMO ESTABA
process and process.kill()



