
def generate_frame_list(filename, x):
    frame_list = [f'"frame_{i:03d}.png"' for i in range(x)]

    with open(filename, 'w') as file:
        file.write(f"[{', '.join(frame_list)}]")

def print_dict(dictionary, indent=0):
    for key, value in dictionary.items():
        if isinstance(value, dict):
            print("\t" * indent + f"{key}:")
            print_dict(value, indent + 1)
        elif isinstance(value, list):
            print("\t" * indent + f"{key}:")
            print('\t' * indent, end='')
            print('[')
            for i in range(0, len(value), 7):
                print('\t' * (indent + 1), end='')
                print(*value[i:i + 7])
            print('\t' * indent, end='')
            print(']')
        else:
            print("\t" * indent + f"{key}:\t{value}")

def is_valid_chname(character):
    return character.isalpha() or character.isdigit() or character == '_'
def extract_value(namespace, config):
    index = 0
    eof = len(namespace)

    conf = config
    while index < eof:

        key = ''
        while index < eof and is_valid_chname(namespace[index]):
            key += namespace[index]
            index += 1
        conf = conf[key] if key in conf else None
        if conf == None:
            print(f"key:{key} in {namespace} not found")
            exit(1)

        if index < eof and namespace[index] == '.':
            index += 1



    return conf


