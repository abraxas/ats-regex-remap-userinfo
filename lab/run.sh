#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-ats-regex-remap-userinfo}"
export PYTHONUNBUFFERED=1
chmod +x poc.py

LABEL="ats-regex-remap-userinfo"
WITNESS="ATS-REGEX-REMAP-USERINFO-WITNESS"
IMAGE="ats-10.2.0-lab:local"
LOCK="/tmp/ats-10.2.0-lab.lock"
SRC_DIR="../../client-reviews/trafficserver/src"
ATS_URL="http://127.0.0.1:18730"

down() {
  echo "== docker compose down -v =="
  docker compose -p "${COMPOSE_PROJECT_NAME}" down -v --remove-orphans || true
}

trap down EXIT

fail_setup() {
  local reason="$1"
  echo "FAIL ${LABEL} ${reason} ${WITNESS}" | tee poc-last-run.txt
  docker compose -p "${COMPOSE_PROJECT_NAME}" logs --no-color --tail=120 || true
  exit 1
}

ensure_image() {
  echo "== ensure ${IMAGE} =="
  if docker image inspect "${IMAGE}" >/dev/null 2>&1; then
    echo "IOC image-present ${IMAGE}"
    return 0
  fi
  echo "IOC image-build ${IMAGE} lock=${LOCK}"
  python3 - "${IMAGE}" "${SRC_DIR}" "${PWD}/Dockerfile.base" "${LOCK}" <<'PY'
import fcntl
import os
import subprocess
import sys

image, src, dockerfile, lock_path = sys.argv[1:]
os.makedirs(os.path.dirname(lock_path) or ".", exist_ok=True)
with open(lock_path, "a", encoding="utf-8") as handle:
    fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
    inspect = subprocess.run(
        ["docker", "image", "inspect", image],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if inspect.returncode == 0:
        print(f"IOC image-present {image}", flush=True)
        sys.exit(0)
    print(f"IOC image-build {image}", flush=True)
    subprocess.run(["docker", "build", "-f", dockerfile, "-t", image, src], check=True)
PY
}

echo "== docker compose down (clean) =="
down
ensure_image

echo "== docker compose up --build =="
up_ok=0
for attempt in $(seq 1 12); do
  if docker compose -p "${COMPOSE_PROJECT_NAME}" up --build -d; then
    up_ok=1
    break
  fi
  echo "IOC compose-up-retry attempt=${attempt}"
  sleep 20
  down
done
if [[ "${up_ok}" != 1 ]]; then
  fail_setup "compose-up-failed"
fi

echo "== wait ATS ${ATS_URL} Host lab-slash.example /ok =="
ready=0
for i in $(seq 1 90); do
  body="$(
    python3 - <<'PY' || true
import socket
payload = (
    b"GET /ok HTTP/1.1\r\n"
    b"Host: lab-slash.example\r\n"
    b"Connection: close\r\n"
    b"\r\n"
)
try:
    with socket.create_connection(("127.0.0.1", 18730), timeout=3) as sock:
        sock.sendall(payload)
        data = b"".join(iter(lambda: sock.recv(4096), b""))
    print(data.decode("utf-8", "replace"))
except OSError as exc:
    print(f"ERR {exc}")
PY
  )"
  if grep -q "GOOD" <<<"${body}" && ! grep -q "${WITNESS}" <<<"${body}"; then
    ready=1
    echo "IOC ats-ready attempt=${i}"
    break
  fi
  echo "IOC ats-wait attempt=${i}"
  sleep 2
done
if [[ "${ready}" != 1 ]]; then
  docker compose -p "${COMPOSE_PROJECT_NAME}" logs --no-color --tail=160 ats || true
  fail_setup "ats-not-ready"
fi

echo "== poc.py =="
set +e
python3 ./poc.py | tee poc-last-run.txt
rc=${PIPESTATUS[0]}
set -e

if ! tail -n1 poc-last-run.txt 2>/dev/null | grep -qE '^(SUCCESS|FAIL) '; then
  echo "FAIL ${LABEL} poc-exit=${rc} ${WITNESS}" >> poc-last-run.txt
  rc=1
fi

exit "${rc}"
