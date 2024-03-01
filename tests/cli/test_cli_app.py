import unittest

from click.testing import CliRunner
from src.cli.cli_commands import start_app


class CliAppTest(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_run(self):
        result = self.runner.invoke(start_app, input="run\nexit\n")
        self.assertIn("Running task", result.output)

    def test_add_path(self):
        result = self.runner.invoke(start_app, input="add path\nexit\n")
        self.assertIn("Adding path", result.output)

    def test_exit(self):
        result = self.runner.invoke(start_app, input="exit\n")
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Exiting the application.", result.output)

    def test_invalid_command(self):
        result = self.runner.invoke(start_app, input="invalid\n")
        self.assertIn("Invalid command. Please try again.", result.output)
        result = self.runner.invoke(start_app, input="exit\n")
        self.assertEqual(result.exit_code, 0)
