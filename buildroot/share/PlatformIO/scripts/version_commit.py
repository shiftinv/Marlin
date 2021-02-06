import os
import re

if os.path.exists('.version_dev'):
    # just set to 'dev' if the file exists, to avoid rebuilding the entire project with every new commit while developing
    version = 'dev'
else:
    # don't want to rely on a git binary being available, reading the files manually works alright as well
    with open('.git/HEAD', 'r') as f:
        head = f.read().strip()

    if re.match(r'^[a-fA-F0-9]+$', head):
        # if it matched, we're in 'detached HEAD' state and already got the commit hash
        git_commit = head
    else:
        # if it didn't match, read the commit hash from the associated ref file
        assert head.startswith('ref: ')
        ref_path = head.split('ref: ')[1]

        with open(os.path.join('.git', ref_path), 'r') as f:
            git_commit = f.read().strip()
    version = git_commit[:10]

version = 'bugfix-2.0.x+{}'.format(version)
# prevent overflow in dwin.cpp: `DWIN_WIDTH - strlen(SHORT_BUILD_VERSION) * MENU_CHR_W`
assert len(version) <= 272 // 8

print('-D SHORT_BUILD_VERSION=\\"{}\\"'.format(version))
