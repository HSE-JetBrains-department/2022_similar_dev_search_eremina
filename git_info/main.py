import click

from git_summarizer import process_repo


@click.command()
@click.option("--repo-dir", "-repo")
@click.option("--repo-url", "-url", default=None)
@click.option("--data-dir", "-data")
def get_input(repo_dir: str, repo_url: str, data_dir: str):
    """
    CLI to receive input with necessary paths to repository and directories
    :param repo_dir:    directory with local repository
    :param repo_url:    url of remote repository
    :param data_dir:    directory to save output data
    """
    click.echo(f"Processing repository from {repo_dir} and saving data to {data_dir}")
    process_repo(repo_dir, data_dir, repo_url)


if __name__ == "__main__":
    get_input()
