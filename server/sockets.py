from settings import (
    SERVER_PORT,
    SCAN_PORT,
    SOCK_BUFFER,
    SOCK_SERVER_SECRET,
    SOCK_ENCODING,
    SOCK_CHECKSTATUS,
    SOCK_CHECKSTATUS_ACK,
    SOCK_SEP,
    SOCK_TIMEOUT,
    SOCK_OK,
    SCREEN_DIR,
)
import socket
import threading
import logging
import time
import ipaddress
import asyncio
from typing import Callable, Tuple, List, Optional
import pdb

logger = logging.getLogger()


class ser_sock:
    def __init__(self) -> None:
        self.sock = socket.socket(
            socket.AddressFamily.AF_INET, socket.SocketKind.SOCK_STREAM
        )
        self.listening: bool = False
        self.clients: dict[
            str, Tuple[threading.Thread, socket.socket, Optional[Callable]]
        ] = {}

    def start_listen(self, listen_ip, update_clients: Callable[[list], None]) -> bool:
        logger.info(f"start listening on ip {listen_ip}:{SERVER_PORT}")
        self.update_clients: Callable[[list], None] = update_clients
        try:
            self.sock.bind((listen_ip, SERVER_PORT))
            self.sock.settimeout(SOCK_TIMEOUT)
            self.sock.listen()
            self.listening = True
            self.listen_thread: threading.Thread = threading.Thread(target=self.listen)
            self.listen_thread.start()
            return True
        except socket.error as e:
            logger.error("Socket Start error")
            logger.error(e)
            return False
            # Handle the bind error

    def add_ip(self, ip: str):
        logger.info(f"adding single ip {ip}")
        self.scan_ip(ip)
        self.update_clients_wrap()
        return True

    def get_screen(self, ip: str, show_screen: Callable[[str], None]) -> bool:
        c = self.clients[ip]
        if not c:
            return False
        logger.info(f"requesting screenshot from {ip}")
        c[1].send("SCREENSHOT".encode(SOCK_ENCODING))
        self.clients[ip] = (c[0], c[1], show_screen)
        return True

    def listen(self):
        logger.info("accepting connections from socket")
        while self.listening:
            try:
                conn, addr = self.sock.accept()
                conn.settimeout(SOCK_TIMEOUT)
                t = threading.Thread(target=self.handel_client, args=(conn, addr[0]))
                logger.info(f"accepted from {addr}")
                self.clients[addr[0]] = (t, conn, None)
                self.update_clients_wrap()
                t.start()
            except socket.timeout:
                # logger.debug("socket timeout accept")
                pass
            except socket.error as e:
                # Handle the exception or break the loop if needed
                logger.error("Lieten Accept error")
                logger.error(e)
                break

    def close(self):
        if not self.listening:
            return
        logger.info("closing socket")
        self.listening = False
        time.sleep(SOCK_TIMEOUT + 0.2)
        di = self.clients.items()
        self.clients.clear()
        time.sleep(SOCK_TIMEOUT + 0.2)
        for addr, val in di:
            try:
                logger.info(f"closeing connection {addr}")
                val[1].send(b"")
                val[1].close()
            except socket.error as e:
                logger.error("while disconnecting client list")
                logger.error(e)
        self.sock.close()

    def send_reset(self, ip: str):
        c = self.clients[ip]
        if not c:
            return False
        logger.info(f"sending reset for {ip}")
        c[1].send("RESET".encode(SOCK_ENCODING))
        self.close_client(ip)
        return True

    def send_shutdown(self, ip: str):
        c = self.clients[ip]
        if not c:
            return False
        logger.info(f"sending shutdown for {ip}")
        c[1].send("SHUTDOWN".encode(SOCK_ENCODING))
        self.close_client(ip)
        return True

    def scan_network(self, network_ip: str) -> bool:
        logger.info(f"scanning network {network_ip}")
        network = ipaddress.IPv4Network(network_ip, strict=False)
        self.scan_ips([x for x in network])
        return True

    def scan_ip(self, ip):
        try:
            s = socket.socket(
                socket.AddressFamily.AF_INET, socket.SocketKind.SOCK_STREAM
            )
            s.settimeout(1)
            r = s.connect_ex((str(ip), SCAN_PORT))
            if r == 0:
                logger.info(f"sending hello to ip {ip}")
                s.send(SOCK_SERVER_SECRET.encode(SOCK_ENCODING))
            s.close()
        except socket.error:
            pass

    def scan_ips(self, ip_list):
        threads = []
        for ip in ip_list:
            thread = threading.Thread(target=self.scan_ip, args=(ip,))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

    def handel_client(self, conn: socket.socket, addr: str):
        while addr in self.clients:
            try:
                msg = conn.recv(SOCK_BUFFER)
                if not msg:
                    logger.info(f"Client {addr} disconnected")
                    break
                msg = msg.decode(SOCK_ENCODING)
                if msg == SOCK_CHECKSTATUS:
                    logger.info(f"status check {addr}")
                    conn.send(SOCK_CHECKSTATUS_ACK.encode(SOCK_ENCODING))
                if msg == "SCREENSEND":
                    try:
                        conn.settimeout(None)
                        logger.info(f"reciving screen from {addr}")
                        conn.send(SOCK_OK.encode(SOCK_ENCODING))
                        msg = conn.recv(SOCK_BUFFER).decode(SOCK_ENCODING)
                        file_size = int(msg)
                        conn.send(SOCK_OK.encode(SOCK_ENCODING))
                        with open(SCREEN_DIR / f"{addr}_screen.png", "wb") as file:
                            current_size = 0
                            while current_size < file_size:
                                msg = conn.recv(SOCK_BUFFER)
                                file.write(msg)
                                current_size += len(msg)
                        logger.info(f"recived screen from {addr}")
                        conn.send(SOCK_OK.encode(SOCK_ENCODING))
                        if self.clients[addr][2]:
                            c = self.clients[addr]
                            if c[2]:
                                c[2](SCREEN_DIR / f"{addr}_screen.png")
                    except socket.error as e:
                        logger.error(f"error while reciveing screenshot from {addr}")
                        logger.error(e)
                    finally:
                        conn.settimeout(SOCK_TIMEOUT)
            except socket.timeout:
                # logger.debug(f"socket timeout {addr}")
                pass
            except socket.error as e:
                logger.error("client handel error")
                logger.error(e)
                break

    def update_clients_wrap(self):
        self.update_clients([x for x in self.clients.keys()])

    def close_client(self, ip: str) -> bool:
        try:
            logger.info(f"closeing client {ip}")
            c = self.clients[ip]
            if c:
                c[1].close()
                del self.clients[ip]
                self.update_clients_wrap()
            return True
        except Exception:
            return False
