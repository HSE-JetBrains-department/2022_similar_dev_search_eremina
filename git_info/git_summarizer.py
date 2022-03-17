import difflib
import json
import logging
import traceback

from typing import Tuple, List
from dulwich import porcelain
from dulwich.objects import ShaFile
from dulwich.repo import Repo


def into_lines(repo: Repo, sha: ShaFile) -> List[str]:
    """
    Gets list of lines from specific repository object
    :param repo: Repository to extract data from
    :param sha: Object sha
    :return: List of lines of provided object
    """
    return repo.get_object(sha).data.decode().splitlines()


def get_diffs(repo: Repo, old_sha: ShaFile, new_sha: ShaFile) -> Tuple[int, int]:
    """
    Gets information about diffs in particular change
    :param repo: repository path
    :param old_sha: object old version sha
    :param new_sha: object new version sha
    :return: tuple with number of added strings as first value and deleted as second
    """
    diffs = difflib.unified_diff(into_lines(repo, old_sha), into_lines(repo, new_sha))
    added, deleted = 0, 0
    for diff in diffs:
        match diff[:1]:
            case ["+", char] if char != "+":
                added += 1
            case ["-", char] if char != "-":
                deleted += 1
    return added, deleted


def save_commits_data(repo_dir: str, output_file: str) -> None:
    """
    Saves data about commits in provided directory
    :param repo_dir: repository path
    :param output_file: file path to save output data
    """
    repo = Repo(repo_dir)
    for entry in repo.get_walker():
        if len(entry.commit.parents) < 2:
            repo_url = f"""{repo.get_config().get(("remote", "origin"), "url")}"""
            commit_sha = entry.commit.id.decode()
            author = entry.commit.author.decode()
            stats = {
                "added": 0,
                "deleted": 0
            }

            for change in entry.changes():
                file = (change.new.path or change.old.path).decode()
                try:
                    match (change.old.sha, change.new.sha):
                        case (None, new_sha):
                            stats["added"] += len(into_lines(repo, new_sha))
                        case (old_sha, None):
                            stats["deleted"] += len(into_lines(repo, old_sha))
                        case (old_sha, new_sha):
                            stats["added"], stats["deleted"] = get_diffs(repo, old_sha, new_sha)

                    with open(output_file, "a") as f:
                        json.dump({
                            "repository": repo_url,
                            "sha": commit_sha,
                            "file": file,
                            "author": author,
                            "added": stats["added"],
                            "deleted": stats["deleted"]
                        }, f)
                        f.write("\n")
                except (IOError, UnicodeError):
                    logging.error(
                        f"""
                            Error in repo: {repo_url}\n
                            Commit: {commit_sha}\n
                            In file: {file}\n
                            {traceback.format_exc()}
                        """)


def process_repo(repo_dir: str, output_file: str, url: str = None) -> None:
    """
    Helper to call repository data processing
    :param repo_dir: directory with local repository
    :param url: url of remote repository
    :param output_file: file path to save output data
    """
    if url:
        porcelain.clone(url, repo_dir)

    save_commits_data(repo_dir, output_file)
