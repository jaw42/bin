#!/bin/bash
# Created:  Mon 13 Apr 2015
# Modified: Mon 13 Apr 2015
# Author:   Josh Wainwright
# Filename: git-pull.sh

git fetch ${1:-origin} ${2:-master}
echo
git merge ${1:-origin}/${2:-master}
echo
# git log HEAD..${1:-origin}/${2:-master} --oneline
git log --oneline --graph ORIG_HEAD..
