def parse(tokens, action, goto, start_state, table_grammar):
    stack = [start_state]
    idx = 0
    errors = []

    while idx < len(tokens):
        current_state = stack[-1]
        current_token = tokens[idx]

        try:
            action_entry = action[current_state][current_token]
        except KeyError:
            errors.append(f"Syntactic error at token {current_token} (index {idx}) in state {current_state}")
            break

        if action_entry[0] == 'S':
            stack.append(action_entry[1])
            idx += 1
        elif action_entry[0] == 'R':
            production_number = action_entry[1]
            production = table_grammar[production_number - 1]
            head, body = production

            for _ in body:
                stack.pop()
            new_state = stack[-1]

            try:
                stack.append(goto[new_state][head])
            except KeyError:
                errors.append(f"Grammatical error after reducing with production {production_number} in state {new_state}")
                break
        elif action_entry[0] == 'ACC':
            return "Accepted", errors

    if not errors:
        errors.append("Parsing finished with unaccepted tokens")

    return "Rejected", errors