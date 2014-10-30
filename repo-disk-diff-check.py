#!/usr/bin/env python

import boto
import subprocess
import socket
import tempfile
import shutil
import repos as repos

def send_sns_msg_aws(topic_arn, mesg, topicstring):
    try:
        c = boto.connect_sns()
        c.publish(topic_arn, mesg, topicstring)
    except Exception , e:
        print e

hostname = socket.gethostname()

for cur_repo in repos.repos_to_check:
    tempdir = tempfile.mkdtemp()
    subprocess.call([ 'git', 'clone', '--quiet', '--recursive', cur_repo['repo-path'], tempdir ])
    diff_output = subprocess.check_output([ 'git', '--git-dir=' + tempdir + '/.git', '--work-tree=' + cur_repo['deploy-path'], 'diff' ])
    shutil.rmtree(tempdir)

    if diff_output:
        subject = 'WARNING : Uncommitted Changes in ' + cur_repo['repo-path'] + ' on ' + hostname
        send_sns_msg_aws(
                         'arn:aws:sns:us-east-1:344420214229:repo_out_of_sync',
                         diff_output,
                         subject 
                        )
        send_sns_msg_aws(
                         'arn:aws:sns:us-east-1:344420214229:unb_lib_developers',
                         subject,
                         subject 
                         )
