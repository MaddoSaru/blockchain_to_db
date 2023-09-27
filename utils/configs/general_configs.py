import os
from dotenv import load_dotenv

load_dotenv()

ddbb_config = {
    "host" : "127.0.0.1",
    "user" : "root",
    "password" : os.getenv("MYSQL_ROOT_PASS"),
    "database" : "test"
}
