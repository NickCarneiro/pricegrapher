#!/bin/bash
git stash
git pull
git stash pop
./manage.py collectstatic