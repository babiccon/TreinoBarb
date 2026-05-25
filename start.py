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


def kill_port(port):
    """Mata qualquer processo usando a porta especificada (Windows)."""
    try:
        import subprocess
        result = subprocess.run(
            f'for /f "tokens=5" %a in (\'netstat -aon ^| find ":{port}" ^| find "LISTENING"\') do taskkill /f /pid %a',
            shell=True, capture_output=True, timeout=3
        )
    except Exception:
        pass


def start_web():
    port = 8081

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT_DIR)

    # Tenta iniciar na porta 8081; se falhar, mata o processo que a ocupa e tenta novamente
    for attempt in range(2):
        try:
            server = http.server.HTTPServer(("0.0.0.0", port), handler)
            break
        except OSError:
            if attempt == 0:
                print(f"  Porta {port} ocupada. Liberando...")
                kill_port(port)
                import time; time.sleep(1)
            else:
                print(f"  Erro: Não foi possível iniciar na porta {port}.")
                return

    url_local = f"http://localhost:{port}/index.html"

    print()
    print("  ========================================================")
    print("               Treino Tracker -- Servidor")
    print("  ========================================================")
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
