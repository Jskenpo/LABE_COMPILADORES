from collections import defaultdict

def compute_first(grammar, non_terminals, terminals):
    first = defaultdict(set)

    # Regla 1: Si X es un terminal, entonces FIRST(X) = {X}
    for terminal in terminals:
        first[terminal] = {terminal}

    # Regla 2 y 3: Calcular FIRST para los no terminales
    while True:
        updated = False
        for non_terminal in non_terminals:
            old_first = first[non_terminal].copy()
            for production in grammar:
                if production[0] == non_terminal:
                    first[non_terminal].update(first_of_production(first, production[1], terminals))
            if old_first != first[non_terminal]:
                updated = True
        if not updated:
            break

    return first

def first_of_production(first, production, terminals):
    result = set()
    for symbol in production:
        if symbol in terminals:
            result.add(symbol)
            break
        else:
            result.update(first[symbol])
            if '#' not in first[symbol]:
                break
    else:
        result.add('#')
    return result



def compute_follow(grammar, non_terminals, start_symbol, first):
    follow = defaultdict(set)
    follow[start_symbol] = {'$'}

    while True:
        updated = False
        for non_terminal in non_terminals:
            old_follow = follow[non_terminal].copy()
            for production in grammar:
                if non_terminal in production[1]:
                    for i, symbol in enumerate(production[1]):
                        if symbol == non_terminal:
                            if i + 1 < len(production[1]):
                                follow[non_terminal].update(first[production[1][i + 1]])
                                if '#' in first[production[1][i + 1]]:
                                    follow[non_terminal].update(follow[production[0]])
                                    follow[non_terminal].remove('#')
                            else:
                                follow[non_terminal].update(follow[production[0]])
            if old_follow != follow[non_terminal]:
                updated = True
        if not updated:
            break

    return follow

def indexGrammar(grammar):
    productions = {}
    contador = 1
    for i in grammar:
        elemento = i[1]
        productions[contador] = elemento
        contador += 1
    return productions

def indexGrammar2(grammar):
    productions = {}
    contador = 1
    for i in grammar:
        productions[contador] = i  # Mantener la tupla (head, body)
        contador += 1
    return productions

def construir_tabla_SLR(automata, follow, terminales, no_terminales, productions):
    action = defaultdict(dict)
    goto = defaultdict(dict)
    sr_conflicts = []  # Lista para almacenar conflictos shift/reduce
    rr_conflicts = []  # Lista para almacenar conflictos reduce/reduce

    for state in automata.states:
        for prod in state.productions:
            head, body = prod
            dot_pos = body.index('·')

            # Regla de desplazamiento (shift)
            if dot_pos < len(body) - 1 and body[dot_pos + 1] in terminales:
                symbol = body[dot_pos + 1]
                next_state = next(s for s in automata.states if (state, symbol, s) in automata.transitions)
                if symbol in action[state.name] and action[state.name][symbol][0] == 'R':
                    sr_conflicts.append((state.name, symbol))
                action[state.name][symbol] = ('S', next_state.name)

            # Regla de reducción (reduce)
            if dot_pos == len(body) - 1 and head != "S":
                for symbol in follow[head]:
                    for key, value in productions.items():
                        if value == body:
                            if symbol in action[state.name] and action[state.name][symbol][0] == 'S':
                                sr_conflicts.append((state.name, symbol))
                            elif symbol in action[state.name] and action[state.name][symbol][0] == 'R':
                                rr_conflicts.append((state.name, symbol))
                            action[state.name][symbol] = ('R', key)

            # Aceptación (accept)
            if head == "S" and dot_pos == len(body) - 1:
                action[state.name]['$'] = ('ACC',)

        # Rellenar tabla GOTO
        for non_term in no_terminales:
            next_state = next((s for s in automata.states if (state, non_term, s) in automata.transitions), None)
            if next_state:
                goto[state.name][non_term] = next_state.name

    return action, goto, sr_conflicts, rr_conflicts



        

def imprimir_tabla_SLR(action, goto):
    print("Tabla ACTION:")
    for state in action:
        for symbol in action[state]:
            print(f"Action[{state}, {symbol}] = {action[state][symbol]}")
    
    print("\nTabla GOTO:")
    for state in goto:
        for non_term in goto[state]:
            print(f"Goto[{state}, {non_term}] = {goto[state][non_term]}")