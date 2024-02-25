from click.testing import CliRunner
from src.cli.cli_commands import start_app


def test_run():
    runner = CliRunner()
    result = runner.invoke(start_app, ["run"])
    assert result.exit_code == 0
    assert "Running task" in result.output


def test_add_path():
    runner = CliRunner()
    result = runner.invoke(start_app, ["add path"])
    assert result.exit_code == 0
    assert "Adding path" in result.output


def test_exit():
    runner = CliRunner()
    result = runner.invoke(start_app, ["exit"])
    assert result.exit_code == 0
    assert "Exiting the application." in result.output


def test_invalid_command():
    runner = CliRunner()
    result = runner.invoke(start_app, ["invalid"])
    assert result.exit_code == 0
    assert "Invalid command" in result.output
