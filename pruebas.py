from collections import defaultdict

# Definición de las tablas `ACTION` y `GOTO`
action = defaultdict(dict, {
    'I0': {'LPAREN': ('S', 'I4'), 'ID': ('S', 'I5')},
    'I1': {'$': ('ACC',), 'PLUS': ('S', 'I6')},
    'I3': {'PLUS': ('R', 4), 'TIMES': ('R', 4), 'RPAREN': ('R', 4), '$': ('R', 4)},
    'I5': {'PLUS': ('R', 6), 'TIMES': ('R', 6), 'RPAREN': ('R', 6), '$': ('R', 6)},
    'I10': {'PLUS': ('R', 3), 'TIMES': ('R', 3), 'RPAREN': ('R', 3), '$': ('R', 3)},
    'I6': {'LPAREN': ('S', 'I4'), 'ID': ('S', 'I5')},
    'I8': {'RPAREN': ('S', 'I11'), 'PLUS': ('S', 'I6')},
    'I11': {'PLUS': ('R', 5), 'TIMES': ('R', 5), 'RPAREN': ('R', 5), '$': ('R', 5)},
    'I7': {'LPAREN': ('S', 'I4'), 'ID': ('S', 'I5')},
    'I9': {'PLUS': ('R', 1), '$': ('R', 1), 'RPAREN': ('R', 1), 'TIMES': ('S', 'I7')},
    'I4': {'LPAREN': ('S', 'I4'), 'ID': ('S', 'I5')},
    'I2': {'PLUS': ('R', 2), '$': ('R', 2), 'RPAREN': ('R', 2), 'TIMES': ('S', 'I7')}
})

goto = defaultdict(dict, {
    'I0': {'expression': 'I1', 'term': 'I2', 'factor': 'I3'},
    'I6': {'term': 'I9', 'factor': 'I3'},
    'I7': {'factor': 'I10'},
    'I4': {'expression': 'I8', 'term': 'I2', 'factor': 'I3'}
})

# Gramática indexada
productions = {
    1: ['expression', 'PLUS', 'term'],
    2: ['term'],
    3: ['term', 'TIMES', 'factor'],
    4: ['factor'],
    5: ['LPAREN', 'expression', 'RPAREN'],
    6: ['ID']
}

def parse(input_tokens, action, goto, productions):
    stack = ['I0']
    tokens = input_tokens + ['$']
    index = 0

    while True:
        state = stack[-1]
        token = tokens[index]

        if token in action[state]:
            action_value = action[state][token]
            action_type = action_value[0]

            if action_type == 'S':  # Shift
                next_state = action_value[1]
                stack.append(token)
                stack.append(next_state)
                index += 1
            elif action_type == 'R':  # Reduce
                production_number = action_value[1]
                production = productions[production_number]
                head = production[0]
                body_length = len(production)  # Length of the production body
                stack = stack[:-2 * body_length]  # Pop the body length (times 2) from the stack
                current_state = stack[-1]
                stack.append(head)
                if head in goto[current_state]:
                    stack.append(goto[current_state][head])
                else:
                    raise SyntaxError(f"Unexpected non-terminal '{head}' in state '{current_state}'")
            elif action_type == 'ACC':  # Accept
                return "Input accepted"
        else:
            raise SyntaxError(f"Unexpected token '{token}' in state '{state}'")

# Ejemplo de uso
input_tokens = ['ID', 'PLUS', 'ID', 'TIMES', 'ID']
try:
    result = parse(input_tokens, action, goto, productions)
    print(result)
except SyntaxError as e:
    print(e)
