def generate_frame_list(filename, x):
    frame_list = [f'"frame_{i:03d}.png"' for i in range(x)]

    with open(filename, 'w') as file:
        file.write(f"[{', '.join(frame_list)}]")

def print_dict(dictionary, indent=0):
    for key, value in dictionary.items():
        if isinstance(value, dict):
            print("\t" * indent + f"{key}:")
            print_dict(value, indent + 1)
        else:
            print("\t" * indent + f"{key}:\t{value}")

def extract_value(namespace, config):
    index = 0
    eof = len(namespace)

    conf = config
    while index < eof:

        key = ''
        while index < eof and namespace[index].isalpha():
            key += namespace[index]
            index += 1
        conf = conf[key] if key in conf else None
        if conf == None:
            print(f"key:{key} in {namespace} not found")
            exit(1)

        if index < eof and namespace[index] == '.':
            index += 1



    return conf
