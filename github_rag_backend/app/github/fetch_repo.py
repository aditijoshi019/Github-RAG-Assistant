import git
import os

def clone_repo(repo_url):
    repo_name = repo_url.split("/")[-1]
    path = f"repos/{repo_name}"

    if not os.path.exists(path):
        git.Repo.clone_from(repo_url, path)

    return path