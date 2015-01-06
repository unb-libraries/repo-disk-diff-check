#!/usr/bin/env python

import subprocess
import os
import socket
import tempfile
import shutil
import repos as repos

ec2_sns_sender_binpath = '/var/opt/ec2-sns-sender/sns_send'
hostname = socket.gethostname()

def send_sns(topic_id, subject, message):
    DEVNULL = open(os.devnull, 'w')
    subprocess.call([ ec2_sns_sender_binpath, '-t', topic_id, '-s', subject, '-m', message ], stdout=DEVNULL, stderr=DEVNULL)

for repo in repos.repos_to_check:
    tempdir = tempfile.mkdtemp()
    if 'branch' in repo:
      subprocess.call([ 'git', 'clone', '--quiet', '--recursive', '-b', repo['branch'], repo['repo-path'], tempdir ])
    else:
      subprocess.call([ 'git', 'clone', '--quiet', '--recursive', repo['repo-path'], tempdir ])
    diff_output = subprocess.check_output([ 'git', '--git-dir=' + tempdir + '/.git', '--work-tree=' + repo['deploy-path'], 'diff' ])
    shutil.rmtree(tempdir)

    if diff_output:
        subject = 'WARNING : Uncommitted Changes in ' + repo['repo-path'] + ' on ' + hostname
        send_sns('arn:aws:sns:us-east-1:344420214229:repo_out_of_sync', subject, diff_output)
        send_sns('arn:aws:sns:us-east-1:344420214229:unb_lib_developers', subject, subject)
