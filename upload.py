#!/usr/bin/env python3
import requests
import time
import pdb
import os
import sys
import argparse
from sh.contrib import git

"""
create repo
curl -X POST --header "Authorization: Bearer <token>" https://api.github.com/user/repos -d '{"name":"repo-name","description":"description","private":true,"is_template":false}'

delete repo

curl -X DELETE --header "Authorization: Bearer <token>" https://api.github.com/repos/joebb97/repo

push to github
git remote add github <github url with personal account token>
                      https://<username>:<token>@github.com/<owner>/<repository-name>.git
                      git@github.com:joebb97/eecs491project1.git
git branch -a
iterate over branches
    git checkout <branchname>
    git push github <branchname>
    git checkout master / main
"""

def create_repos(dry_run):
    github_pat = os.environ.get('GITHUB_PAT')
    if not github_pat:
        print("Need github personal account token")
        sys.exit(1)
    repos_dir = os.path.join('.', 'joebb')
    os.chdir(repos_dir)
    repos = os.listdir()
    for repo in repos:
        print(f'creating repo {repo}')
        repo_url = 'https://api.github.com/user/repos'
        if dry_run:
            continue

        resp = requests.post(
            repo_url,
            json={'name': repo, 'description': 'migrated from eecs gitlab', 'private': True, 'is_template': False},
            headers={'Authorization': f'Bearer {github_pat}'}
        )
        if not resp.ok:
            print('bad status', resp.status_code, resp.json())
        
        time.sleep(1)

def push_repos(dry_run):
    github_pat = os.environ.get('GITHUB_PAT')
    if not github_pat:
        print("Need github personal account token")
        sys.exit(1)
    repos_dir = os.path.join('.', 'joebb')
    os.chdir(repos_dir)
    repos = os.listdir()
    for repo in repos:
        print(f'processing {repo}')
        os.chdir(repo)

        try:
            git('remote', 'add', 'github', f'git@github.com:joebb97/{repo}.git')
        except:
            pass

        git('remote', 'set-url', 'github', f'git@github.com:joebb97/{repo}.git')

        branches = git('branch', '-a')
        gitlab_branches = filter_gitlab_branches(branches)
        print(gitlab_branches)

        for branch in gitlab_branches:
            git('checkout', branch)
            print(f'pushing repo {repo} with git push github {branch}')
            if dry_run:
                continue
            print(git('push', 'github', branch, _err_to_out=True))

        os.chdir('..')
        if not dry_run:
            time.sleep(1)

def filter_gitlab_branches(lines):
    gitlab_branches = []

    for line in lines.splitlines():
        if 'HEAD' in line:
            continue
        split = line.split('remotes/origin/')
        if len(split) == 1:
            continue
        gitlab_branches.append(split[1])

    return gitlab_branches

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                        prog='upload.py',
                        description='uploads gitlab checkouts')
    parser.add_argument('--create-repos', action='store_true')
    parser.add_argument('--push-repos', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    if args.create_repos:
        create_repos(args.dry_run)
    elif args.push_repos:
        push_repos(args.dry_run)
    else:
        print('unknown option')
        sys.exit(1)

