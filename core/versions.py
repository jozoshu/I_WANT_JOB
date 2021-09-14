import os

import git
from git import TagReference


class VersionManager:

    def __init__(self):
        self.repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        tag = self.get_latest_tag_from_repo()
        self.tag_name = tag.name

    def get_latest_tag_from_repo(self) -> TagReference:
        repo = git.Repo(self.repo_dir)
        return repo.tags[-1]

    @property
    def version(self):
        return self._version
