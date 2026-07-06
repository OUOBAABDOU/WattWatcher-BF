import os
import sys

os.environ["DATABASE_URL"] = "sqlite:///wattwatcher_local.db"
sys.path.insert(0, "backend")

import app as watt_app

watt_app.load_sample_if_empty(watt_app.app)
watt_app.app.run(debug=False, use_reloader=False, host="127.0.0.1", port=5000)
