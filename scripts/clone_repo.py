"""
Clone a git repository to a local directory.
"""

import sys
from pathlib import Path
from git import Repo


REPOS_DIR = Path("data/repos")


def clone_repo(repo_url: str, repo_name: str) -> str:

    repo_path = REPOS_DIR / repo_name
    if repo_path.exists():
        print(f"Repository already exists: {repo_path}")
        print(f"Next step:")
        print(f"py -m scripts.index_repo {repo_name}")
        sys.exit(0)
        

    REPOS_DIR.mkdir(parents=True, exist_ok=True)

    Repo.clone_from(repo_url, repo_path)
    return str(repo_path)

if __name__ == "__main__":
    

    if len(sys.argv) != 3:
        print("Usage: py -m scripts.clone_repo <repo_url> <repo_name>")
        sys.exit(1)
    
    
    repo_url = sys.argv[1]
    repo_name = sys.argv[2]

    cloned_path = clone_repo(repo_url, repo_name)

    print(f"Repository cloned to: {cloned_path}")
    print(f"Next step:")
    print(f"py -m scripts.index_repo {repo_name}")