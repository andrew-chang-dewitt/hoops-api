"""
Hoops - A Web API for a personal budgeting application.

Run by either calling `python -m hoops.app` or 
`python -m flask` from the directory this file is in.

© 2021 Andrew Chang-DeWitt
Source distributed under an MIT License.
"""
from flask import Flask

app = Flask(__name__)


@app.route("/")
def index() -> dict[str, bool]:
    """Check API status at index."""
    return {
        "status": True
    }


if __name__ == "__main__":
    app.run()
