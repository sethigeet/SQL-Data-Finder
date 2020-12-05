from gui import create_app
from gui.config import Config

app = create_app(config_class=Config)

if __name__ == '__main__':
    app.run(debug=True)
