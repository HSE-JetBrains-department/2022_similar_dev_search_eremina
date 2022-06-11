import click
from github import Github
from stargazers import StargazersExtractor
from summarizer import GitSummarizer


@click.command()
@click.option("--repo-dir", "-dir")
@click.option("--repo-url", "-url")
@click.option("--output-file", "-output")
@click.option("--github-token", "-token")
@click.option("--repo-threshold", "-threshold", type=int, default=10)
def get_input(repo_dir: str, repo_url: str, output_file: str, github_token: str, repo_threshold: int):
    """
    CLI to receive input with necessary paths to repository and directories
    :param repo_dir: directory to save repositories
    :param repo_url: url of remote repository to extract data from
    :param output_file: path to file for output data
    :param github_token: github access token
    :param repo_threshold: number of most common repositories to be selected for similar developers search
    """
    click.echo(f"Processing repository {repo_url} and saving data to {output_file}")

    repos = StargazersExtractor(repo_url, github_token, repo_threshold).get_top_repositories()
    GitSummarizer(repositories=list(map(lambda repo: Github(github_token).get_repo(repo).clone_url, repos)),
                  clone_dir=repo_dir,
                  output_file=output_file).extract_info()


if __name__ == "__main__":
    get_input()
