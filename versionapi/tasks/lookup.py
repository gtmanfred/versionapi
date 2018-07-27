# -*- coding: utf-8 -*-
import git
import shutil

from versionapi.celery import tasks

import version_check.config
import version_check.core


@tasks.task(bind=True)
def search(self, repository='saltstack/salt', pr_num=None, commit_id=None):
    path = f'gitrepos/{self.request.id}/'
    repo = git.Repo.clone_from(f'git://github.com/{repository}.git', bare=True, to_path=path)
    version_check.config.GIT_DIR = f'--git-dir={path}'
    ret = version_check.core.search(pr_num=pr_num, commit=commit_id)
    shutil.rmtree(path)
    return ret
