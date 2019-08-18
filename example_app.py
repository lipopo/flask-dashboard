from flask import Flask
from flask_dashboard import mount_dashboard_to

app = Flask(__name__)
mount_dashboard_to(app)

@app.route('/')
def main():
    return 'hello'


if __name__ == "__main__":
    app.run(port=5551, debug=True)
