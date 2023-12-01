
def load(path):
    data = ''
    try:
        with open(path, 'r') as file:
            data = file.read()
    except FileNotFoundError:
        print(f"The file '{path}' was not found.")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    return data