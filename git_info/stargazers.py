import logging
import time
from collections import defaultdict
from datetime import datetime
from typing import List

from github import Github, NamedUser, RateLimitExceededException


class StargazersExtractor:
    def __init__(self, repo_url: str, token: str):
        """
        :param repo_url: url of remote repository to extract data from
        :param token: access token for github api
        """
        self.repos_threshold = 10

        self.stars = defaultdict(int)
        self.url = repo_url
        self.github = Github(token)

    def process_repo(self) -> List[str]:
        """
        Processes repository's stargazers and saves data about their starred repositories
        :return: most starred repositories' names
        """
        repo = self.github.get_repo("/".join(self.url.split("/")[-2:]))
        for stargazer in repo.get_stargazers():
            self.process_starred(stargazer)
        return sorted(self.stars, key=self.stars.get, reverse=True)[:min(len(self.stars), self.repos_threshold)]

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
