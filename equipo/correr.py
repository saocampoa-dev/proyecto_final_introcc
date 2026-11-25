# correr.py  ---  la pelicula de la cueva
# Uso:  python3 correr.py            la pelicula del nivel del guion, con narrador
#       python3 correr.py 2          la pelicula de otro nivel (sin narrador: el guion es de un nivel)
#       python3 correr.py cueva      la misma pelicula con el ambiente de cueva oscura
#       python3 correr.py guion      escribe voces/guion.txt, la lista de frases para grabar
#       python3 correr.py tabla      la tabla de todos los niveles
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "Recursos"))
sys.path.insert(0, os.path.join(AQUI, "..", "mundos", "cueva"))        # <- el mundo
sys.path.insert(0, os.path.join(AQUI, "..", "ejemplo_hacienda"))       # las generaciones 1 y 2 son LAS MISMAS de la hacienda

import mundo
from bitacora import Bitacora
from animar3d import animar3d, escribir_guion
import g1_a_ciegas
import g2_con_hilo
import g3_rastreador
import guion

GENERACIONES = [   # (agente, nombre, descripcion, eventos por segundo en la pelicula)
    (g1_a_ciegas, "Generación 1 · a ciegas", "Camina hasta que no puede más y solo entonces pregunta si sigue vivo.", 25),
    (g2_con_hilo, "Generación 2 · con hilo", "Pregunta después de cada paso. Cae, pero se devuelve por el hilo y prueba otro camino.", 8),
    (g3_rastreador, "Generación 3 · rastreador", "Lleva una libreta. Siente la brisa, deduce dónde está el pozo y cuenta el aceite.", 3),
]
VOCES = os.path.join(AQUI, "voces")
orden = sys.argv[1] if len(sys.argv) > 1 else ""

if orden == "guion":
    escribir_guion(guion.GUION, VOCES)
    sys.exit(0)

if orden == "tabla":
    print("%-6s %-28s %10s %8s %10s %8s %6s" % ("nivel", "generacion", "soluciones", "pasos", "tropiezos", "deduce", "poda"))
    for nivel in mundo.casos():
        caso = mundo.cargar(nivel)
        for (g, nombre, _, _) in GENERACIONES:
            bit = Bitacora(nombre, grabar=False)
            s = g.resolver(mundo, caso, bit)
            c = bit.cuenta
            print("%-6s %-28s %10d %8d %10d %8d %6d" % (nivel, nombre, s, c["avanzar"], c["rechazar"], c["deducir"], c["podar"]))
    sys.exit(0)

ambiente = "cueva" if orden == "cueva" else "sala"
nivel = int(orden) if orden.isdigit() else guion.NIVEL
caso = mundo.cargar(nivel)
caso["ambiente"] = ambiente
capitulos = []
for (g, nombre, descripcion, ritmo) in GENERACIONES:
    bit = Bitacora(nombre)
    s = g.resolver(mundo, caso, bit)
    c = bit.cuenta
    print("%-28s soluciones %d | pasos %d, tropiezos %d, deduce %d, poda %d" % (nombre, s, c["avanzar"], c["rechazar"], c["deducir"], c["podar"]))
    capitulos.append((bit, nombre, descripcion, ritmo))
animar3d(capitulos, lambda estado: mundo.dibujar(caso, estado), os.path.join(AQUI, "cueva_%s_nivel%d.html" % (ambiente, nivel)),
         titulo=caso["titulo"], max_eventos=1300,
         pregunta="Hay pozos que no se ven y el farol tiene el aceite contado. ¿Por dónde llega Pixie al cofre?",
         guion=guion.GUION if nivel == guion.NIVEL else None, voces=VOCES)
