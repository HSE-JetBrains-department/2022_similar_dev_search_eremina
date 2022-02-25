import json

from dulwich import porcelain
from dulwich.repo import Repo


def save_commits_data(repo_dir: str, data_dir: str):
    """
    Saves data about commits in provided directory
    :param repo_dir:    repository path
    :param data_dir:    directory to save data
    :return:
    """
    repo = Repo(repo_dir)
    commits = {}
    for entry in repo.get_walker():
        if len(entry.commit.parents) < 2:
            sha = entry.commit.id.decode()
            author = entry.commit.author.decode()
            message = entry.commit.message.decode()
            commits[sha] = {
                'author': author,
                'message': message
            }
            # TODO: process changes
    with open(data_dir + "/commits.json", "w") as f:
        json.dump(commits, f)


def process_repo(repo_dir: str, data_dir, url=None):
    """
    Helper to call repository data processing
    :param repo_dir:    directory with local repository
    :param url:         url of remote repository
    :param data_dir:    directory to save output data
    """
    if url:
        porcelain.clone(url, repo_dir)

    save_commits_data(repo_dir, data_dir)
