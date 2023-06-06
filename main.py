from app import app
from setup import setup

if __name__ == "__main__":
    setup()
    app.run(host="0.0.0.0", port=8788, debug=True)
