import sys
from os.path import abspath, dirname

# finding root directory
current_dir = dirname(abspath(__file__))
# set project root directory
project_root = abspath(dirname(current_dir))

# add root directory on sys.path
sys.path.insert(0, project_root)

from shopping_mall import app

if __name__ == '__main__':
    app.run(debug=True)
