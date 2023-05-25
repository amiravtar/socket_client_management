import socket
import logging
from pathlib import Path
from settings import (
    SCAN_PORT,
    SOCK_SEP,
    SOCK_SERVER_SECRET,
    SOCK_ENCODING,
    SOCK_CHECKSTATUS,
    SOCK_CHECKSTATUS_ACK,
    SOCK_BUFFER,
    SERVER_PORT,
    SOCK_TIMEOUT,
    SOCK_OK,
)
from PIL import ImageGrab
import os
import pdb

log_file = (Path(__file__).parent) / "logs" / "app.log"
logger = logging.basicConfig(
    filename=log_file,
    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)
logger = logging.getLogger()

listenning = False


def start_listen():
    n = input("Enter systems ip:")

    sock = socket.socket(socket.AddressFamily.AF_INET, socket.SocketKind.SOCK_STREAM)

    sock.bind((n, SCAN_PORT))
    logger.info(f"start listening on ip {n}:{SCAN_PORT}")
    sock.listen(1)
    sock.settimeout(SOCK_TIMEOUT)
    while listenning:
        try:
            conn, addr = sock.accept()
            logger.info(f"connected from {addr[0]}")
            msg = conn.recv(SOCK_BUFFER)
            if msg.decode(SOCK_ENCODING) == SOCK_SERVER_SECRET:
                conn.close()
                sock.close()
                return addr[0]
        except socket.timeout:
            pass
        except socket.error as e:
            logger.error("socket accept error")
            logger.error(e)
            return None


def connect_to_server(ip: str):
    logger.info(f"connecting to server {ip}")
    con = socket.socket(socket.AddressFamily.AF_INET, socket.SocketKind.SOCK_STREAM)
    con.connect((ip, SERVER_PORT))
    con.settimeout(SOCK_TIMEOUT)
    con.send(SOCK_CHECKSTATUS.encode(SOCK_ENCODING))
    while True:
        try:
            con.settimeout(SOCK_TIMEOUT)
            msg = con.recv(SOCK_BUFFER)
            if not msg:
                logger.info("connection closed")
                break
            msg = msg.decode(SOCK_ENCODING)
            if msg == SOCK_CHECKSTATUS:
                logger.info("status check")
                con.send(SOCK_CHECKSTATUS_ACK.encode(SOCK_ENCODING))
            elif msg == "REEST":
                con.close()
                if os.name == "posix":  # Linux or macOS
                    os.system("sudo shutdown -r now")
                elif os.name == "nt":  # Windows
                    os.system("shutdown /r /t 0")

            elif msg == "SHUTDOWN":
                con.close()
                if os.name == "posix":  # Linux or macOS
                    os.system("sudo shutdown -h now")
                elif os.name == "nt":  # Windows
                    os.system("shutdown /s /t 0")
            elif msg == "SCREENSHOT":
                con.settimeout(None)
                logger.info("sending screenshot")
                con.send("SCREENSEND".encode(SOCK_ENCODING))
                msg = con.recv(SOCK_BUFFER).decode(SOCK_ENCODING)
                if msg != SOCK_OK:
                    logger.info("server didnt accept screenshot")
                    continue
                # Capture the entire screen
                screenshot = ImageGrab.grab()
                img_path = (Path(__file__).parent) / "screen.png"
                screenshot.save(img_path)
                size = os.path.getsize(img_path)
                con.send(str(size).encode(SOCK_ENCODING))
                msg = con.recv(SOCK_BUFFER).decode(SOCK_ENCODING)
                if msg != SOCK_OK:
                    logger.info("error from server while sending screen")
                    continue
                with open(img_path, "rb") as file:
                    line = file.read(SOCK_BUFFER)
                    while line:
                        con.send(line)
                        line = file.read(SOCK_BUFFER)
                msg = con.recv(SOCK_BUFFER).decode(SOCK_ENCODING)
                if msg != SOCK_OK:
                    logger.info("server didnt recive screenshot")
                    continue
                logger.info("screenshot sent")

        except socket.timeout:
            pass
        except socket.error as e:
            logger.error("client server error")
            logger.error(e)
            break
    logger.info("disconnecting")
    con.close()


if __name__ == "__main__":
    listenning = True
    ip = start_listen()
    if ip:
        connect_to_server(ip)
    else:
        logger.error("no ip from listen")
    logger.info("exiting")
