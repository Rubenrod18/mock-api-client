"""Main module runs the application.

The module runs the application on differents
configurations ( dev, prod, testing, etc ), run commands, etc.

"""

import os

from dotenv import load_dotenv

from app import create_app

load_dotenv()

app = create_app(os.getenv('FLASK_CONFIG'))


if __name__ == '__main__':
    app.run()
