#!/usr/bin/env python3
import sys
import time
import json
import os
import subprocess

# To create out.txt I ran the following curl command
"""
curl -X GET --header "PRIVATE-TOKEN: $GITLAB_PAT" 'https://gitlab.eecs.umich.edu/api/v4/projects?membership=true&per_page=100' > out.txt
"""

if __name__ == '__main__':
    gitlab_pat = os.environ.get('GITLAB_PAT')
    if not gitlab_pat:
        print("Need github personal account token")
        sys.exit(1)

    with open('out.txt', 'r') as f:
        repos = json.load(f)

    for repo in repos:
        repo_url = repo.get('http_url_to_repo', None)
        split = repo_url.split('/')
        user = split[-2]
        project = split[-1]
        split[2] = f'joebb:{gitlab_pat}@gitlab.eecs.umich.edu'
        repo_url = '/'.join(split)
        try:
            os.mkdir(user)
        except:
            pass
        
        subprocess.run(['git', '-C', user, 'clone', repo_url])

        time.sleep(1)

# After I ran this script I did some manual moves of some repos
# created by other people to match my naming scheme
"""
cd joebb/
mv c4cs-w17-rpn c4cs-w17-rpn2
mv dotfiles/ dotfiles-old
mv project5/ eecs280project5
mv project1 eecs281project1
cd ..
mv szehnder/p5-search-engine joebb/eecs485project5
mv szehnder/p4-mapreduce joebb/eecs485project4
mv szehnder/373-otomatone joebb/
mv szehnder/p3-insta485-clientside joebb/eecs485project3
mv szehnder/p2-insta485-serverside joebb/eecs485project2
mv mdeegan/project4 joebb/eecs280project4
mv mdeegan/project3 joebb/eecs280project3
"""
