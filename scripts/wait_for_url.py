import argparse
import sys
import time
from urllib.error import URLError
from urllib.request import urlopen


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--interval", type=float, default=1.0)
    return parser.parse_args()


def main():
    args = parse_args()
    deadline = time.time() + args.timeout

    while time.time() < deadline:
        try:
            with urlopen(args.url, timeout=5) as response:
                if 200 <= response.status < 500:
                    print(f"URL is ready: {args.url}")
                    return 0
        except URLError:
            pass
        time.sleep(args.interval)

    print(f"Timeout waiting for {args.url}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
