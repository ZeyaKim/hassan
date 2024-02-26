from click.testing import CliRunner
from src.cli.cli_commands import start_app
import pytest
import threading
from functools import wraps


class TimeoutException(Exception):
    pass


def timeout(seconds):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = [None]

            def run():
                result[0] = func(*args, **kwargs)

            thread = threading.Thread(target=run)
            thread.start()
            thread.join(seconds)

            if thread.is_alive():
                raise TimeoutException(f"Test timed out after {seconds} seconds")
            return result[0]

        return wrapper

    return decorator


@pytest.fixture
def cli_runner():
    runner = CliRunner()
    return runner


@timeout(2)
def test_run(cli_runner):
    result = cli_runner.invoke(start_app, input="run\nexit\n")
    assert "Running task" in result.output


@timeout(2)
def test_add_path(cli_runner):
    result = cli_runner.invoke(start_app, input="add_path\nexit\n")
    assert "Adding path" in result.output


@timeout(2)
def test_exit(cli_runner):
    result = cli_runner.invoke(start_app, input="exit\n")
    assert result.exit_code == 0
    assert "Exiting the application." in result.output


@timeout(2)
def test_invalid_command(cli_runner):
    result = cli_runner.invoke(start_app, input="invalid\nexit\n")
    assert "Invalid command. Please try again." in result.output
    assert result.exit_code == 0
