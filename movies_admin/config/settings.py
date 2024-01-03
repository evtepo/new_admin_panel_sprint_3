from pathlib import Path
from dotenv import load_dotenv
from split_settings.tools import include

import os


load_dotenv()

include(
    "components/*.py",
)

if DEBUG:
    INSTALLED_APPS.append("debug_toolbar_force")
    MIDDLEWARE.append("debug_toolbar_force.middleware.ForceDebugToolbarMiddleware")
