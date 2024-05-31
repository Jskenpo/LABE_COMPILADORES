def parse(input_tokens, action, goto, productions):
    stack = ['I0']
    tokens = input_tokens + ['$']
    index = 0

    while True:
        state = stack[-1]
        token = tokens[index]

        if token not in action[state]:
            raise SyntaxError(f"Unexpected token '{token}' in state '{state}'")

        action_value = action[state][token]
        action_type = action_value[0]

        if action_type == 'S':  # Shift
            next_state = action_value[1]
            stack.append(token)
            stack.append(next_state)
            index += 1
        elif action_type == 'R':  # Reduce
            production_number = action_value[1]
            production = productions[production_number][1]
            head = productions[production_number][0]
            body_length = len(production)  # Include the head of the production
            stack = stack[:-2 * body_length]
            current_state = stack[-1]
            #sa
            stack.append(head)
            if head in goto[current_state]:
                stack.append(goto[current_state][head])
            else:
                raise SyntaxError(f"Unexpected non-terminal '{head}' in state '{current_state}'")
        elif action_type == 'ACC':  # Accept
            return "Input accepted"
        else:
            raise SyntaxError(f"Invalid action {action_value} in state '{state}'")
