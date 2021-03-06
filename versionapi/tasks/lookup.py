# -*- coding: utf-8 -*-
import filelock
import git
import os
import pathlib

from versionapi.celeryapp import tasks

import version_check.config
import version_check.core


@tasks.task(bind=True, max_retries=None)
def search(self, repository='saltstack/salt', pr_num=None, commit_id=None):
    ret = {
        'repo': repository,
        'rev': f'#{pr_num}' or commit_id,
    }
    path = f'gitrepos/{repository}'
    lock_path = f'{path}.lock'
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    try:
        with filelock.FileLock(lock_path, timeout=0):
            if not os.path.isdir(f'{path}/.git'):
                git.Repo.clone_from(f'git://github.com/{repository}.git', to_path=path)
        version_check.config.GIT_DIR = f'--git-dir={path}/.git'
        ret.update(version_check.core.search(pr_num=pr_num, commit=commit_id))
        if commit_id:
            ret['rev'] = commit_id
        return ret
    except TimeoutError:
        self.retry(countdown=5)
