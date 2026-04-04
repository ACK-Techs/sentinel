from sentinel_cli.cli.app import main


def test_config_command_returns_zero(capsys) -> None:
    code = main(["config", "--profile", "local"])
    captured = capsys.readouterr()
    assert code == 0
    assert '"active_profile"' in captured.out


def test_doctor_command_returns_zero(capsys) -> None:
    code = main(["doctor", "--profile", "local"])
    captured = capsys.readouterr()
    assert code == 0
    assert '"mcp"' in captured.out
