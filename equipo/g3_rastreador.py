# g3_rastreador.py  ---  generacion 3 en la cueva: saber antes de pisar
#
# Este agente SI conoce la cueva, y lleva una LIBRETA con lo que va sabiendo. Lo
# que anota en la libreta es verdad de la cueva, asi que no se borra al retroceder:
# de un intento al siguiente, Pixie sabe mas. Usa cuatro reglas:
#
#   Regla 1 (sin brisa).  Si aqui NO hay brisa, entonces todas las vecinas son seguras.
#   Regla 2 (la brisa).   Si aqui hay brisa, alguna vecina es un pozo. Si de las vecinas
#                         solo UNA no esta anotada como segura, el pozo esta ahi.
#   Regla 3 (el aceite).  Si desde una casilla el cofre queda mas lejos que los pasos
#                         de aceite que sobran, entonces por ahi no se llega.
#   Regla 4 (la caida).   Si cayo en una casilla, ahi hay un pozo. (Esta se aprende a golpes.)
#
# Con las reglas 2 y 3 PODA pasos sin darlos.


def resolver(mundo, caso, bit):
    libreta = {"seguras": set([caso["entrada"]]), "pozos": set(), "brisas": []}
    return buscar(mundo, caso, mundo.inicio(caso), libreta, bit)


def foto(estado, libreta):
    return {"camino": estado["camino"], "peligro": sorted(libreta["pozos"]), "seguras": sorted(libreta["seguras"])}


def percibir(mundo, caso, aqui, libreta):
    """Aplica las reglas 1 y 2 con lo que se percibe aqui. Devuelve los pozos recien deducidos."""
    libreta["seguras"].add(aqui)
    if mundo.brisa(caso, aqui):
        if aqui not in libreta["brisas"]:
            libreta["brisas"].append(aqui)
    else:
        for v in mundo.vecinas(caso, aqui):                 # Regla 1
            libreta["seguras"].add(v)
    nuevos = []
    for b in libreta["brisas"]:                             # Regla 2, con todo lo que ya se sabe
        dudosas = []
        for v in mundo.vecinas(caso, b):
            if v not in libreta["seguras"]:
                dudosas.append(v)
        if len(dudosas) == 1 and dudosas[0] not in libreta["pozos"]:
            libreta["pozos"].add(dudosas[0])
            nuevos.append(dudosas[0])
    return nuevos


def buscar(mundo, caso, estado, libreta, bit):
    if mundo.completo(caso, estado) and mundo.viola(caso, estado) == "":
        bit.registrar("solucion", foto(estado, libreta), mundo.respuesta(caso, estado))
        return 1
    aqui = estado["camino"][-1]
    for pozo in percibir(mundo, caso, aqui, libreta):
        bit.registrar("deducir", foto(estado, libreta),
                      "la brisa solo puede venir de la fila %d, columna %d" % (pozo[0] + 1, pozo[1] + 1))
    total = 0
    for paso in mundo.opciones(caso, estado):
        if paso in libreta["pozos"]:                                              # Regla 2 o 4
            bit.registrar("podar", foto(estado, libreta), "ahí hay un pozo: no da ese paso")
            continue
        if mundo.distancia(paso, caso["cofre"]) > mundo.aceite(caso, estado) - 1:  # Regla 3
            bit.registrar("podar", foto(estado, libreta), "por ahí no alcanza el aceite")
            continue
        nuevo = mundo.aplicar(caso, estado, paso)
        falla = mundo.viola(caso, nuevo)
        if falla == "":
            bit.registrar("avanzar", foto(nuevo, libreta), mundo.decir(caso, paso))
            total = total + buscar(mundo, caso, nuevo, libreta, bit)
            bit.registrar("retroceder", foto(estado, libreta))
        else:
            if falla == "cayó en un pozo":
                libreta["pozos"].add(paso)                                        # Regla 4
            bit.registrar("rechazar", foto(nuevo, libreta), falla)
    return total
