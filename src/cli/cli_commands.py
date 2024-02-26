import click


def add_path():
    """경로를 추가하는 함수입니다."""
    click.echo("Adding path")


def run():
    """작업을 실행하는 함수입니다."""
    click.echo("Running task")


# 명령어와 관련 함수를 매핑
command_map = {
    "add path": add_path,
    "run": run,
}


class InvalidCommandError(Exception):
    """유효하지 않은 명령어가 입력되었을 때 발생하는 예외입니다."""

    pass


@click.command()
def start_app():
    """대화형 CLI 애플리케이션을 시작합니다."""
    try:
        while True:
            click.echo("Available commands: add path, run, exit")
            command = click.prompt("Enter a command")
            if command == "exit":
                click.echo("Exiting the application.")
                break
            elif command in command_map:
                command_map[command]()
            else:
                raise InvalidCommandError()
    except InvalidCommandError:
        click.echo("Invalid command. Please try again.")
        start_app()
