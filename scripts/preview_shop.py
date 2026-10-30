#!/usr/bin/env python3
"""Serve the repository and open the shop at /, so benchmark links also work."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit


class PreviewHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlsplit(self.path)
        if parsed.path == '/':
            self.send_response(302)
            target = '/examples/rural-shop-demo/'
            if parsed.query:
                target += '?' + parsed.query
            self.send_header('Location', target)
            self.end_headers()
            return
        super().do_GET()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8775)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    server = ThreadingHTTPServer(('127.0.0.1', args.port), partial(PreviewHandler, directory=str(root)))
    print(f'Shop: http://127.0.0.1:{args.port}/', flush=True)
    print(f'Benchmark: http://127.0.0.1:{args.port}/review/shop-benchmark/', flush=True)
    server.serve_forever()
