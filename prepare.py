def generar_gramatica_argumentada(gramatica_original):
    # Crear una nueva gramática argumentada con el nuevo estado inicial
    inicial = []
    primerNT = next(iter(gramatica_original))
    inicial.append('·')
    inicial.append(primerNT)
    gramatica_argumentada = [
        ("S", inicial)
    ]

    # Copiar las producciones de la gramática original a la gramática argumentada
    for no_terminal, producciones in gramatica_original.items():
        for produccion in producciones:
            gramatica_argumentada.append((no_terminal, produccion))

    return gramatica_argumentada


# ---------------------CERRADURA----------------------------
'''
ConjuntoDeElementos CERRADURA(I) {
    J = I;
    repeat
        for ( cada elemento A → α·Bβ en J )
            for ( cada producción B → γ de G )
                if ( B → ·γ no está en J )
                    agregar B → ·γ a J;
    until no se agreguen más elementos a J en una ronda;
    return J;
 }

'''

def cerradura(I, gramatica):
    J = I
    while True:
        for elemento in J:
            no_terminal = elemento[0]
            produccion = elemento[1]
            punto = produccion.index('·')
            if punto < len(produccion) - 1:
                simbolo = produccion[punto + 1]
                for produccion in gramatica:
                    if produccion[0] == simbolo:
                        if (simbolo, ['·'] + produccion[1]) not in J:
                            J.append((simbolo, ['·'] + produccion[1]))
        if J == I:
            break
        I = J
    return J


# ---------------------MOVER----------------------------

'''
ConjuntoDeElementos Ir_A(I, X) {
    J = ConjuntoDeElementos vacío
    for (cada elemento A -> alpha ° X beta en I) {
        mover A -> alpha X ° beta a J
    }
    return Cerradura(J)

'''

def mover(I, X, gramatica):
    J = []
    for elemento in I:
        no_terminal = elemento[0]
        produccion = elemento[1]
        punto = produccion.index('·')
        if punto < len(produccion) - 1 and produccion[punto + 1] == X:
            J.append((no_terminal, produccion[:punto] + [X, '·'] + produccion[punto + 2:]))
    return cerradura(J, gramatica)

grammar = [
    ('S', ['·', 'expression']), 
    ('expression', ['expression', 'PLUS', 'term']), 
    ('expression', ['term']), 
    ('term', ['term', 'TIMES', 'factor']), 
    ('term', ['factor']), 
    ('factor', ['LPAREN', 'expression', 'RPAREN']), 
    ('factor', ['ID'])
]

def terminals(grammar, non_terminals):
    terminals = set()
    for production in grammar:
        for symbol in production[1]:
            if symbol != '·' and symbol not in non_terminals:
                terminals.add(symbol)

    return terminals

def non_terminals(grammar):
    non_terminals = set()
    for production in grammar:
        if production[0] == 'S':
            continue
        else :
            non_terminals.add(production[0])

    return non_terminals