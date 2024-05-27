
from graphviz import Digraph
from prepare import *
class Estado:
    def __init__(self, name):
        self.name = name
        self.productions = []

class LRAutomata:
    def __init__(self ):
        self.inicial = None
        self.states = set()
        self.transitions = set()

    def crearTransicion(self, state, symbol, new_state):
        #hacer tupla con estado origen, transicion y estado destino
        transition = (state, symbol, new_state)
        self.transitions.add(transition)
    
    def crearEstado(self, state):
        self.states.add(state)

    def setInicial(self, state):
        self.inicial = state


#---------------------construccion de automata ----------------------------

'''
void elementosLR0() {
            C = {Cerradura({S' -> °S})}
            repeat {
                for (cada conjunto de elementos I en C) {
                    for (cada símbolo gramatical X) {
                        if (Ir_A(I, X) no está en C) {
                            agregar Ir_A(I, X) a C
                        }
                    }
                }
            } until (no se agregan nuevos conjuntos de elementos)
        }

'''


def conjunto_a_cadena(conjunto):
    cadena = ""
    for produccion in sorted(conjunto):
        cadena += f"{produccion[0]} -> {''.join(produccion[1])}\n"
    return cadena

def elementosLR0(gramatica):
    contador = 0
    nombreEstado = "I" + str(contador)
    C = []
    I = [gramatica[0]]
    C.append(cerradura(I, gramatica))
    automata = LRAutomata()
    estadoInicial = Estado(nombreEstado)
    estadoInicial.productions = C[0]
    automata.crearEstado(estadoInicial)
    automata.setInicial(estadoInicial)
    contador += 1

    while True:
        nuevos_conjuntos = []
        for conjunto in C:
            for simbolo in conjunto:
                if simbolo[1][-1] != '·':
                    index = simbolo[1].index('·')
                    nuevo_conjunto = cerradura(mover(conjunto, simbolo[1][index + 1], gramatica), gramatica)
                    nuevo_conjunto_str = conjunto_a_cadena(nuevo_conjunto)
                    if all(conjunto_a_cadena(estado.productions) != nuevo_conjunto_str for estado in automata.states):
                        nombreEstado = "I" + str(contador)
                        nuevoEstado = Estado(nombreEstado)
                        nuevoEstado.productions = nuevo_conjunto
                        automata.crearEstado(nuevoEstado)
                        nuevos_conjuntos.append(nuevo_conjunto)
                        contador += 1
                    estadoActual = next(estado for estado in automata.states if conjunto_a_cadena(estado.productions) == conjunto_a_cadena(conjunto))
                    nuevoEstado = next((estado for estado in automata.states if conjunto_a_cadena(estado.productions) == nuevo_conjunto_str), None)
                    automata.crearTransicion(estadoActual, simbolo[1][index + 1], nuevoEstado)

        if not nuevos_conjuntos:
            break
        C.extend(nuevos_conjuntos)

    return automata

def graficarAutomata(automata, nombre):
    dot = Digraph(comment=nombre)
    dot.attr('node', shape='square')  # Establecer la forma de los nodos como cuadrados

    # Flecha apuntando al estado inicial
    dot.node(automata.inicial.name, label=automata.inicial.name, shape='square')
    dot.edge('Inicio', automata.inicial.name)

    for estado in automata.states:
        # Mostrar el nombre del estado y las producciones
        producciones_str = "\n".join([f"{produccion[0]} -> {''.join(produccion[1])}" for produccion in estado.productions])
        dot.node(estado.name, label=f"{estado.name}\n{producciones_str}", shape='square')

    for transicion in automata.transitions:
        origen = transicion[0]
        simbolo = transicion[1]
        destino = transicion[2]
        dot.edge(origen.name, destino.name, label=simbolo)

    return dot