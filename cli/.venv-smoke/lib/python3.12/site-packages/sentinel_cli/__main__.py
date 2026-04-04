"""Module entrypoint for `python -m sentinel_cli`."""

from sentinel_cli.cli.app import main


if __name__ == "__main__":
    raise SystemExit(main())
