#!/usr/bin/env bash

# BROKEN, DOESN'T WORK
# JUST FOR ARCHIVAL PURPOSES TO SEE HOW BAD IT WAS TO DO IN BASH

list_of_repos=$(cat out.txt | jq -r '.[] | .ssh_url_to_repo')
for repo in ${list_of_repos}; do
    user=$(awk -v repo="${repo}" \
        'BEGIN { where = match (repo, /:(.*)\//); print substr(repo, RSTART + 1, RLENGTH - 2)}')
    project=$(awk -v repo="${repo}" \
        'BEGIN { where = match (repo, /\/.*\.git/); print substr(repo, RSTART + 1, RLENGTH - 5)}')
    echo "cloning ${repo} into ${user}/${project}"
    # sleep 60
    # git clone "${repo}" "${user}/${project}"
done
