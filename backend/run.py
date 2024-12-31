import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from config import Config

app = create_app(Config)

if __name__ == '__main__':
    Config.verify_env_variables()
    app.run(
        host=Config.SERVER_HOST,
        port=Config.SERVER_PORT,
        debug=Config.DEBUG
    )