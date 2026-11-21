#!/usr/bin/env python3
"""Devuelve la IP LAN probable del equipo (o 127.0.0.1 si no hay red)."""
from __future__ import annotations

import socket


def local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip = ""
    try:
        s.connect(("10.255.255.255", 1))
        ip = s.getsockname()[0]
    except OSError:
        pass
    finally:
        s.close()

    if not ip or ip.startswith("127.") or ip == "0.0.0.0":
        try:
            candidata = socket.gethostbyname(socket.gethostname())
            if candidata and not candidata.startswith("127."):
                ip = candidata
        except OSError:
            pass

    return ip or "127.0.0.1"


if __name__ == "__main__":
    print(local_ip())
