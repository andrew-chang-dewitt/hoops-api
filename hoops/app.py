"""
Hoops - A Web API for a personal budgeting application.

Run by either calling `python -m hoops.app` or 
`python -m flask` from the directory this file is in.

© 2021 Andrew Chang-DeWitt
Source distributed under an MIT License.
"""
from typing import Any

from flask import Flask

from transactions import transactions

app = Flask(__name__)


@app.route("/status")
def status() -> dict[str, Any]:
    """Check API status at index."""
    return {
        "ok": True,
    }


app.register_blueprint(transactions)


if __name__ == "__main__":
    app.run()
