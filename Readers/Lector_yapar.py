
import re 

def read_tokens(filename, regular_dict):
    with open(filename, 'r') as f:
        lines = f.readlines()

    tokens_yalp = []
    for line in lines:
        line = line.strip()
        if line.startswith('%token'):
            token = line.split()[1]
            tokens_yalp.append(token)

        if line.startswith('IGNORE'):
            token = line.split()[1]
            if token in tokens_yalp:
                tokens_yalp.remove(token)

    missing_tokens = []
    for token in tokens_yalp:
        if f"return '{token}'" not in regular_dict.values():
            missing_tokens.append(token)
    

    if missing_tokens:
        print(f"Los siguientes tokens en el archivo yalp no se encuentran en el diccionario: {', '.join(missing_tokens)}")
        return missing_tokens, True 
    else:
        print("Todos los tokens en el archivo yalp están presentes en el diccionario.")
        return tokens_yalp, False
    
def read_productions(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    productions = {}
    current_production = None

    for line in lines:
        line = line.strip()

        if line == '%%':
            continue

        if line.endswith(';'):
            production_parts = line[:-1].split(':')
            if len(production_parts) == 2:
                production_name = production_parts[0].strip()
                rules = [rule.strip().split() for rule in production_parts[1].strip().split('|') if rule.strip()]
                productions[production_name] = [rule for rule in rules if rule]
            current_production = None
        elif current_production is not None:
            rules = [rule.strip().split() for rule in line.strip().split('|') if rule.strip()]
            productions[current_production].extend([rule for rule in rules if rule])
        elif line and not line.startswith('/*'):
            production_parts = line.split(':')
            if len(production_parts) == 2:
                production_name = production_parts[0].strip()
                current_production = production_name
                rules = [rule.strip().split() for rule in production_parts[1].strip().split('|') if rule.strip()]
                productions[production_name] = [rule for rule in rules if rule]

    return productions
