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


@click.command()
def start_app():
    """대화형 CLI 애플리케이션을 시작합니다."""
    while True:
        click.echo("Available commands: add path, run, exit")
        command = click.prompt("Enter a command")
        if command == "exit":
            click.echo("Exiting the application.")
            break
        elif command in command_map:
            command_map[command]()
        else:
            click.echo("Invalid command")
