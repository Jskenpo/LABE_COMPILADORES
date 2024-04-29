
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
        return missing_tokens, False