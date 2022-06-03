import logging
import time

from collections import Counter
from datetime import datetime
from github import Github, NamedUser, RateLimitExceededException
from typing import List


class StargazersExtractor:
    def __init__(self, repo_url: str, token: str, threshold: int):
        """
        :param repo_url: url of remote repository to extract data from
        :param token: access token for github api
        :param threshold: number of most common repositories to be selected for next processing
        """
        self.repos_threshold = threshold
        self.stars = Counter()
        self.url = repo_url
        self.github = Github(token)

    def get_top_repositories(self) -> List[str]:
        """
        Processes repository's stargazers and saves data about their starred repositories
        :return: most starred repositories' names
        """
        repo = self.github.get_repo("/".join(self.url.split("/")[-2:]))
        for stargazer in repo.get_stargazers():
            self.process_starred(stargazer)
        return list([name for name, _ in self.stars.most_common(self.repos_threshold)])

    def process_starred(self, stargazer: NamedUser) -> None:
        """
        Saves information about user's starred repositories
        :param stargazer: user to get data from
        """
        starred = None
        while starred is None:
            try:
                starred = stargazer.get_starred()
                for repo in starred:
                    self.stars[repo.full_name] += 1
            except RateLimitExceededException:
                logging.warning("Error while fetching user's starred repos, wait to reconnect")

                reset = self.github.get_rate_limit().search.reset.timestamp()
                now = float(datetime.timestamp(datetime.now()))
                time.sleep(max(0.0, now - reset))
