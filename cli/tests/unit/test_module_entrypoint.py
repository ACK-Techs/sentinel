from sentinel_cli.cli.app import build_parser, main


def test_parser_program_name() -> None:
    assert build_parser().prog == "sentinel-cli"


def test_version_flag(capsys) -> None:
    exit_code = main(["--version"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out.strip() == "0.1.0"
