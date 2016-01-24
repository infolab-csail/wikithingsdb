import os

# whoami
WHOAMI_HOST = os.getenv("WHOAMI_HOST")
WHOAMI_PORT = os.getenv("WHOAMI_PORT")
WHOAMI_USE_AUTH = os.getenv("WHOAMI_USE_AUTH") == "true"
WHOAMI_USERNAME = os.getenv("WHOAMI_USERNAME")
WHOAMI_PASSWORD = os.getenv("WHOAMI_PASSWORD")
