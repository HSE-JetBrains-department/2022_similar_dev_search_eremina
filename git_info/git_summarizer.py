import json
import logging
import traceback
from typing import Tuple

from dulwich import porcelain
from dulwich.objects import ShaFile
from dulwich.repo import Repo
import difflib


def get_diffs(repo: Repo, old_sha: ShaFile, new_sha: ShaFile) -> Tuple[int, int]:
    """
    Gets information about diffs in particular change
    :param repo:        repository path
    :param old_sha:
    :param new_sha:
    :return: tuple with number of added strings as first value and deleted as second
    """
    diffs = difflib.unified_diff(
        repo.get_object(old_sha).data.decode().splitlines(),
        repo.get_object(new_sha).data.decode().splitlines()
    )
    added, deleted = 0, 0
    for diff in diffs:
        match diff[:1]:
            case ['+', char] if char != '+':
                added += 1
            case ['-', char] if char != '-':
                deleted += 1
    return added, deleted


def save_commits_data(repo_dir: str, data_dir: str) -> None:
    """
    Saves data about commits in provided directory
    :param repo_dir:    repository path
    :param data_dir:    directory to save data
    :return:
    """
    repo = Repo(repo_dir)
    for entry in repo.get_walker():
        if len(entry.commit.parents) < 2:
            sha = entry.commit.id.decode()
            author = entry.commit.author.decode()
            stats = {
                "added": 0,
                "deleted": 0
            }

            try:
                for change in entry.changes():
                    path = change.new.path.decode()
                    match (change.old.sha, change.new.sha):
                        case (None, new_sha):
                            stats["added"] += len(repo.get_object(new_sha).data.decode().splitlines())
                        case (old_sha, None):
                            stats["deleted"] += len(repo.get_object(old_sha).data.decode().splitlines())
                        case (old_sha, new_sha):
                            stats["added"], stats["deleted"] = get_diffs(repo, old_sha, new_sha)

                    with open(data_dir + "/commits.json", "a") as f:
                        json.dump({
                            "sha": sha,
                            "path": path,
                            "author": author,
                            "added": stats["added"],
                            "deleted": stats["deleted"]
                        }, f)
            except:
                logging.error(traceback.format_exc())


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
