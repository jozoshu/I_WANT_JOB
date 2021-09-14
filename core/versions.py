import os

import git
from git import TagReference


def get_latest_tag_from_repo() -> TagReference:
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    repo = git.Repo(repo_dir)
    latest_tag = repo.tags[-1]
    assert isinstance(latest_tag, TagReference)
    return latest_tag


def get_version() -> str:
    """Git repo 에 등록된 가장 최신 버전 가져와서 출력"""
    try:
        tag = get_latest_tag_from_repo()
        return f'{tag.name}\n'
    except Exception:
        return '1.0.0\n'
