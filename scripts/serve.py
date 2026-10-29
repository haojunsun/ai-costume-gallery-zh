"""Serve the local gallery on loopback. No dependencies required."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import webbrowser

ROOT = Path(__file__).resolve().parent.parent


class GalleryHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Source snapshots and maintenance scripts are not website assets.
        if any(segment.startswith(".") for segment in self.path.split("/")):
            self.send_error(404)
            return
        super().do_GET()

    def log_message(self, *args):
        pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8949)
    parser.add_argument("--open", action="store_true", help="Open in the default browser")
    args = parser.parse_args()
    handler = partial(GalleryHandler, directory=str(ROOT))
    try:
        server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    except OSError as error:
        parser.exit(1, f"Cannot bind 127.0.0.1:{args.port}: {error}\nTry --port with another local port.\n")
    url = f"http://127.0.0.1:{args.port}/"
    print(f"COSTUME Atlas: {url}\nRoot: {ROOT}\nPress Ctrl+C to stop.", flush=True)
    if args.open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
