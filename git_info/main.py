import click

from git_summarizer import process_repo


@click.command()
@click.option("--repo-dir", "-r")
@click.option("--repo-url", "-u", default=None)
@click.option("--output-file", "-o")
def get_input(repo_dir: str, repo_url: str, output_file: str):
    """
    CLI to receive input with necessary paths to repository and directories
    :param repo_dir: directory with local repository
    :param repo_url: url of remote repository
    :param output_file: path to file for output data
    """
    click.echo(f"Processing repository from {repo_dir} and saving data to {output_file}")
    process_repo(repo_dir, output_file, repo_url)


if __name__ == "__main__":
    get_input()
