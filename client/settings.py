from pathlib import Path

ROOT_DIR = Path(__file__).parent
SERVER_PORT = 8000
SCAN_PORT = 8001
SOCK_BUFFER = 512
SOCK_SEP = "<SEP>"
SOCK_OK = "<OK>"
SOCK_CHECKSTATUS = "<STAT>"
SOCK_CHECKSTATUS_ACK = "<STATACK>"
SOCK_SERVER_SECRET = "<SECRET>"
SOCK_ENCODING = "utf-8"
LOG_FILENAME = ROOT_DIR / "logs" / "app.log"
if not LOG_FILENAME.parent.exists():
    LOG_FILENAME.parent.mkdir(parents=True, exist_ok=True)
    LOG_FILENAME.touch()
SOCK_TIMEOUT = 3
