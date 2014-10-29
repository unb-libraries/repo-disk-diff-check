#!/bin/sh
temp_checkout_path="/tmp/$$"
repository_path=$1
deploy_path=$2

rm -rf "$temp_checkout_path"
mkdir "$temp_checkout_path"
git clone --quiet --recursive "$repository_path" "$temp_checkout_path" > /dev/null

git --git-dir="$temp_checkout_path/.git" --work-tree="$deploy_path" diff
