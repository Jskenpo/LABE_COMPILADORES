
import re 

def read_tokens(filename, regular_dict):
    with open(filename, 'r') as f:
        lines = f.readlines()

    tokens_yalp = []
    ignore_tokens = []

    for line in lines:
        line = line.strip()
        if line.startswith('%token'):
            tokens_on_line = [token.strip() for token in line.split()[1:]]
            tokens_yalp.extend(tokens_on_line)
        elif line.startswith('IGNORE'):
            ignore_tokens_on_line = [token.strip() for token in line.split()[1:]]
            ignore_tokens.extend(ignore_tokens_on_line)

    tokens_yalp = [token for token in tokens_yalp if token not in ignore_tokens]

    missing_tokens = []
    for token in tokens_yalp:
        if f"return {token}" not in regular_dict.values():
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
    read_productions = False
    found_separator = False
    comment_pattern = r"/\*.*?\*/"

    for line in lines:
        line = line.strip()

        # Eliminar comentarios de la línea
        line = re.sub(comment_pattern, "", line)

        if line == '%%':
            read_productions = True
            found_separator = True
            continue

        if not read_productions:
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

    if not found_separator:
        print("No se encontró la sección de producciones (separador '%%')")
        return productions, True

    return productions, False