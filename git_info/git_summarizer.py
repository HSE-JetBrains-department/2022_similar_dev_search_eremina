import json

from dulwich import porcelain
from dulwich.repo import Repo


def save_commits_data(repo_dir, data_dir):
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
    with open(data_dir + '/commits.json', 'w') as f:
        json.dump(commits, f)


def process_repo(repo_dir, data_dir, url=None):
    if url:
        porcelain.clone(url, repo_dir)

    save_commits_data(repo_dir, data_dir)
