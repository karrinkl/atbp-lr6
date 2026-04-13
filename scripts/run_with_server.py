import argparse
import os
import signal
import subprocess
import sys
from urllib.parse import urlparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--server-cmd", required=True)
    parser.add_argument("--target-url", default="http://127.0.0.1:5000/health")
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    return parser.parse_args()


def main():
    args = parse_args()
    if not args.command:
        print("Test command is required", file=sys.stderr)
        return 2

    server = subprocess.Popen(args.server_cmd, shell=True)
    try:
        wait_command = [
            sys.executable,
            "scripts/wait_for_url.py",
            "--url",
            args.target_url,
            "--timeout",
            str(args.timeout),
        ]
        subprocess.check_call(wait_command)

        command = args.command
        if command[0] == "--":
            command = command[1:]
        return subprocess.call(command)
    finally:
        if server.poll() is None:
            if os.name == "nt":
                server.terminate()
            else:
                os.kill(server.pid, signal.SIGTERM)
            server.wait(timeout=20)


if __name__ == "__main__":
    raise SystemExit(main())
