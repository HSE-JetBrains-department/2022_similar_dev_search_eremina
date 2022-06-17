import difflib
import json
import logging
import os.path
import traceback
from typing import Dict, List, Tuple

from dulwich import porcelain
from dulwich.objects import ShaFile
from dulwich.repo import Repo
from enry import get_language
from tree_sitter import Parser

from tree_sitter_utils import LANGUAGES, QUERIES


def _into_lines(repo: Repo, sha: ShaFile) -> List[str]:
    """
    Gets list of lines from specific repository object
    :param repo: Repository to extract data from
    :param sha: Object sha
    :return: List of lines of provided object
    """
    return repo.get_object(sha).data.decode().splitlines()


def _get_file_language(repo: Repo, sha: ShaFile, path: str) -> str:
    """
    Gets language of provided by sha object in repo
    If can not find object, returns "None"
    :param repo: Repository with data
    :param sha: Sha of object in repository
    :param path: Path to file with content
    :return: Language of given object
    """
    match sha:
        case None:
            return "None"
        case sha:
            return get_language(path, repo.get_object(sha).data)


def _get_names_from_source(repo: Repo, sha: ShaFile, language: str) -> Dict[str, List[str]]:
    """
    Gets names of classes, functions and variables for supported languages
    :param repo: Repository with data
    :param sha: Sha of object to be inspected
    :return: Dictionary with lists of corresponding objects' names
    """
    match sha:
        case sha if sha is not None and language in LANGUAGES:
            parser = Parser()
            parser.set_language(LANGUAGES[language])
            code = repo.get_object(sha).data
            return {type: [code[capture[0].start_byte: capture[0].end_byte].decode()
                           for _, capture in
                           enumerate(LANGUAGES[language].query(query).captures(parser.parse(code).root_node))]
                    for type, query in QUERIES[language].items()}
        case _:
            return {"classes": [], "functions": [], "variables": []}


class GitSummarizer:
    def __init__(self, repositories: List[str], clone_dir: str, output_file: str):
        self.repositories = repositories
        self.clone_dir = clone_dir
        self.output_file = output_file

    @staticmethod
    def get_diffs(repo: Repo, old_sha: ShaFile, new_sha: ShaFile) -> Tuple[int, int]:
        """
        Gets information about diffs in particular change
        :param repo: repository path
        :param old_sha: object old version sha
        :param new_sha: object new version sha
        :return: tuple with number of added strings as first value and deleted as second
        """
        diffs = difflib.unified_diff(_into_lines(repo, old_sha), _into_lines(repo, new_sha))
        added, deleted = 0, 0
        for diff in diffs:
            match diff[:1]:
                case ["+", char] if char != "+":
                    added += 1
                case ["-", char] if char != "-":
                    deleted += 1
        return added, deleted

    def save_commits_data(self, path) -> None:
        """
        Saves data about commits in provided directory
        :param path: path to repository
        """
        repo = Repo(path)
        with open(self.output_file, "a") as f:
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
                                    stats["added"] += len(_into_lines(repo, new_sha))
                                case (old_sha, None):
                                    stats["deleted"] += len(_into_lines(repo, old_sha))
                                case (old_sha, new_sha):
                                    stats["added"], stats["deleted"] = GitSummarizer.get_diffs(repo, old_sha, new_sha)
                            language = _get_file_language(repo, new_sha, file)
                            names = _get_names_from_source(repo, new_sha, language.lower())
                            json.dump({
                                "repository": repo_url,
                                "sha": commit_sha,
                                "file": file,
                                "language": language,
                                "author": author,
                                "added": stats["added"],
                                "deleted": stats["deleted"],
                                "classes": names["classes"],
                                "functions": names["functions"],
                                "variables": names["variables"]
                            }, f)
                            f.write("\n")
                        except (IOError, UnicodeError, KeyError):
                            logging.error(
                                f"""
                                    Error in repo: {repo_url}\n
                                    Commit: {commit_sha}\n
                                    In file: {file}\n
                                    {traceback.format_exc()}
                                """)

    def process_repo(self, repo_url: str) -> None:
        """
        Helper to call repository data processing
        :param repo_url: url of remote repository
        """
        path = self.clone_dir + "/" + repo_url.split("/")[-1][:-4]
        if not os.path.isdir(path):
            porcelain.clone(repo_url, path)
        self.save_commits_data(path)

    def extract_info(self) -> None:
        """
        Extracts data for all urls in list of repositories
        """
        for repo_url in self.repositories:
            logging.info(f"Started processing {repo_url}")
            self.process_repo(repo_url)
