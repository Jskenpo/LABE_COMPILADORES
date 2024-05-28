from collections import defaultdict

def compute_first(grammar):
    FIRST = defaultdict(set)
    terminals = set()
    non_terminals = set()

    # Detectar terminales y no terminales
    for head, body in grammar:
        non_terminals.add(head)
        for symbol in body:
            if not symbol.isupper() and symbol not in non_terminals:
                terminals.add(symbol)

    # Inicializar FIRST de terminales
    for terminal in terminals:
        FIRST[terminal].add(terminal)

    # Función para agregar elementos de un conjunto a otro y verificar si hubo cambios
    def add_to_set(destination, source):
        initial_len = len(destination)
        destination.update(source)
        return len(destination) > initial_len

    # Calcular FIRST
    changed = True
    while changed:
        changed = False
        for head, body in grammar:
            if not body:  # Producción ε
                changed |= add_to_set(FIRST[head], {''})
            else:
                for symbol in body:
                    if symbol in terminals:
                        changed |= add_to_set(FIRST[head], {symbol})
                        break
                    else:
                        changed |= add_to_set(FIRST[head], FIRST[symbol] - {''})
                        if '' not in FIRST[symbol]:
                            break
                else:
                    changed |= add_to_set(FIRST[head], {''})

    return FIRST, terminals, non_terminals

def compute_follow(grammar, FIRST, non_terminals):
    FOLLOW = defaultdict(set)
    FOLLOW['S'].add('$')  # El símbolo inicial sigue el símbolo de fin de cadena

    def add_to_set(destination, source):
        initial_len = len(destination)
        destination.update(source)
        return len(destination) > initial_len

    # Calcular FOLLOW
    changed = True
    while changed:
        changed = False
        for head, body in grammar:
            follow_temp = FOLLOW[head].copy()
            for symbol in reversed(body):
                if symbol in non_terminals:
                    changed |= add_to_set(FOLLOW[symbol], follow_temp)
                    if '' in FIRST[symbol]:
                        follow_temp.update(FIRST[symbol] - {''})
                    else:
                        follow_temp = FIRST[symbol].copy()
                else:
                    follow_temp = FIRST[symbol].copy()

    return FOLLOW

# Gramática proporcionada
grammar = [
    ('S', ['·', 'expression']),
    ('expression', ['term', 'expression\'']),
    ('expression\'', ['PLUS', 'term', 'expression\'']),
    ('expression\'', ['']),
    ('term', ['factor', 'term\'']),
    ('term\'', ['TIMES', 'factor', 'term\'']),
    ('term\'', ['']),
    ('factor', ['LPAREN', 'expression', 'RPAREN']),
    ('factor', ['ID'])
]

# Calcular FIRST y FOLLOW
FIRST, terminals, non_terminals = compute_first(grammar)
FOLLOW = compute_follow(grammar, FIRST, non_terminals)

# Mostrar resultados
print("FIRST sets:")
for non_terminal in non_terminals:
    print(f"FIRST({non_terminal}) = {{ {', '.join(FIRST[non_terminal])} }}")

print("\nFOLLOW sets:")
for non_terminal in non_terminals:
    print(f"FOLLOW({non_terminal}) = {{ {', '.join(FOLLOW[non_terminal])} }}")
