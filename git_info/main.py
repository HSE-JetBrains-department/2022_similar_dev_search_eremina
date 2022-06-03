import os

from github import Github
from stargazers import StargazersExtractor
from summarizer import GitSummarizer

if __name__ == "__main__":
    repo_url = os.getenv("repo-url")
    repo_dir = os.getenv("repo-dir")
    output_file = os.getenv("output-file")
    github_token = os.getenv("github-token")
    repo_threshold = int(os.getenv("repo-threshold", "10"))

    print(f"Processing repository {repo_url} and saving data to {output_file}")

    repos = StargazersExtractor(repo_url, github_token, repo_threshold).get_top_repositories()
    GitSummarizer(repositories=list(map(lambda repo: Github(github_token).get_repo(repo).clone_url, repos)),
                  clone_dir=repo_dir,
                  output_file=output_file).extract_info()
