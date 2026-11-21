import argparse
import json
from pathlib import Path
from .scanner import scan_file

def main():
    parser = argparse.ArgumentParser(prog="codesentinel")
    parser.add_argument("command", choices=["scan"])
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    targets = sorted(args.path.rglob("*.py")) if args.path.is_dir() else [args.path]
    findings = [f.as_dict() for file in targets for f in scan_file(file)]
    print(json.dumps(findings, indent=2))
    raise SystemExit(1 if findings else 0)

if __name__ == "__main__":
    main()
