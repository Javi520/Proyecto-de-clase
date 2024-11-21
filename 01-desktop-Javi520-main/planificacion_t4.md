**¿Cómo desarrollar la tarea 4?**

1. Las operaciones de E/S no deben causar el bloqueo de la interfaz:
    - Cuándo ocurre?
        - Ocurre, en nuestra práctica, cuando el servidor HTTP tarda en responder, o por "x" motivo, la petición no es atendida lo suficientemente rápido como para pasar desapercibida por el usuario.
    - Porqué ocurre?
        - El mismo "thread" que ejecuta la interfaz, ejecuta la petición HTTP y espera a recibir para procesarla y seguir atendiendo la interfaz.
    - Cómo solucionarlo?
        Siguiendo un poco la manera de proceder de Cabrero con los ejercicios que hizo en clase, sería lanzar el método/función, en un thread y utilizar los mecanismos de Gtk de callback adecuados.

2. Mecanismos de "feedback" en el sentido en que el usuario sabe que el programa está realizando algo en segundo plano, así como controles que permiten cancelar las operaciones:
    - Como implementarlo y posibles problemas con la implementación actual:
        1. Si implemento la ejecución concurrente de las peticiones HTTP via threads ocurre que "matar" el thread mientras trabaja no es buena idea, lo que sería interesante sería invalidar esa operación; en qué consistiría? En hacer caso omiso de los datos que nos devuelva esa petición, tanto si es exitosa como si no lo es y además revertir los cambios en el modelo que pudiera haber tenido de haberlos tenido. Sabemos que si el modelo nos devuelve unos resultados de "[]" o "[cualquier cosa]", es decir, algo distinto de una excepción, algo ha podido cambiar, ahí desharíamos los cambios, sino no.  
        No usamos "lock" por tanto, es interesante mirar todas las posibles consecuencias que trae esto

3. [Reflexiones personales] Cada petición abrirá una ventana?

Si el usuario clickea para "atizar" al programa, que deberiamos hacer?

Si el usuario clickea, la operación se lanzará concurrentemente pero como se informa al usuario? Que se muestra, no es intrusivo una ventana? Si la operación es exitosa, lo más probable es que ni llegue a verse la ventana, a no ser que no se autocierre la misma

Qué es lo que debe ser concurrente? Las operaciones de E/S, guardado en disco, 
peticiones HTTP, ...

Cómo implementarlo?
- Lanzar la petición o la función de manera concurrente, en un thread mediante
la librería "thread" de python

Peticiones a mayores para la tarea:
