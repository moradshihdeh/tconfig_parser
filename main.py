from parse import *
from helpers import *



def run(filename):
    script = ''
    try:
        with open(filename, 'r') as file:
            script = file.read()
    except FileNotFoundError:
        print(f"The file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    cursor = Cursor(script)
    return parse(cursor)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    result = run('game.cnf')
    #print(result['player'])
    #print(test_global)
    print_dict(result)
    print(extract_value('player.animations.idle.files', result))
    print(extract_value('scene.intro.map.background.filename', result))
    generate_frame_list('list.txt',72)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
