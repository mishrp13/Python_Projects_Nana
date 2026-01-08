#!/bin/bash

for ref in "$@"
do
    if [ "$ref" = "refs/heads/master" ]; then
        TAG="release-$(date +%F)"
        git tag -f "$TAG" refs/heads/master
    fi
done
