"""
Launcher - Treino Tracker
Uso:
    python start.py     → Inicia servidor local + abre navegador
"""

import http.server
import threading
import webbrowser
import functools
import socket
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_local_ip():
    """Retorna o IP local da máquina na rede."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def start_web():
    port = 8081

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT_DIR)

    for attempt_port in range(port, port + 10):
        try:
            server = http.server.HTTPServer(("0.0.0.0", attempt_port), handler)
            port = attempt_port
            break
        except OSError:
            continue
    else:
        print(f"  Erro: Não foi possível encontrar uma porta livre entre {port} e {port + 9}.")
        return

    url_local = f"http://localhost:{port}/index.html"

    print()
    print("  ╔════════════════════════════════════════════════════════╗")
    print("  ║               Treino Tracker — Servidor                ║")
    print("  ╚════════════════════════════════════════════════════════╝")
    print()
    print(f"  PC:      {url_local}")
    print()
    print("  Celular: use o GitHub Pages (HTTPS obrigatorio para o login):")
    print("           https://babiccon.github.io/TreinoBarb/")
    print()
    print("  Pressione Ctrl+C para parar.\n")

    def open_browser():
        import time
        time.sleep(0.5)
        webbrowser.open(url_local)

    threading.Thread(target=open_browser, daemon=True).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Servidor parado.")
        server.shutdown()


if __name__ == "__main__":
    start_web()
