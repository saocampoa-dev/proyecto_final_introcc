# guion.py  ---  lo que dice el narrador de la pelicula
#
# Cada linea es (capitulo, evento, texto). El capitulo se cuenta desde 1. El evento es
# el numero que muestra la pelicula abajo a la izquierda ("evento 12 de 45"); el evento 0
# es el comienzo del capitulo. Para escribir una linea: pausen la pelicula donde pasa algo
# que vale la pena explicar, miren el numero del evento y digan POR QUE el agente hizo eso.
#
# El narrador le habla a Pixie de tu, como un entrenador: burlon, pero de su lado.
# Este guion es del nivel 3. Si cambian de nivel o de agente, los numeros cambian.
NIVEL = 3
GUION = [
    (1, 0, "Hola, Pixie. No sabes nada de esta cueva, así que camina. Ya veremos qué pasa cuando se te apague el farol."),
    (1, 13, "Primer pozo, Pixie. No lo viste venir. Y lo peor: tampoco lo vas a recordar."),
    (2, 0, "Segunda generación. Ahora preguntas después de cada paso, y si algo falla te devuelves por el hilo."),
    (2, 6, "Te caíste igual. Pero bien: seguiste el hilo, volviste a donde estabas y probaste otro camino."),
    (2, 14, "Pixie... ¿otra vez? Tienes hilo, pero no tienes memoria."),
    (3, 0, "Tercera generación. Ahora llevas una libreta: lo que aprendas de la cueva ya no se te olvida."),
    (3, 6, "Una caída. Anótala, Pixie: ese pozo no lo vuelves a pisar."),
    (3, 12, "¿Sientes la brisa? Solo te queda una casilla vecina sin revisar. El pozo tiene que estar ahí."),
    (3, 14, "Eso. No diste el paso, y lo supiste sin caer."),
    (3, 26, "Doce pasos, justo el aceite que tenías. Muy bien, Pixie. Ahora sigue buscando, por si hay otro camino."),
]
