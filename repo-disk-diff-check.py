#!/usr/bin/env python

import json, os, subprocess
from optparse import OptionParser

ec2_sns_sender_binpath = '/var/opt/ec2-sns-sender/sns_send'

def send_sns(topic_id, subject, message):
  DEVNULL = open(os.devnull, 'w')
  subprocess.call([ ec2_sns_sender_binpath, '-t', topic_id, '-s', subject, '-m', message ], stdout=DEVNULL, stderr=DEVNULL)

parser = OptionParser()
parser.add_option('-p', '--print', dest = 'print_only', help = 'Just print the results, no SNS message.', default = False, action = 'store_true')
(options, args) = parser.parse_args()

config = json.load(open(args[0]))

for host, locations in sorted(config['servers'].items()) :
  for location in locations :
    args = 'TMP=`mktemp -d` && cd $TMP && git clone --quiet ' + location['repo']
    if 'branch' in location:
      args += ' -b ' + location['branch']
    args += ' . && sudo git --work-tree=' + location['deploy'] + ' diff'
    if 'ignore' in location:
      args += ' -- ":." ":!' + location['ignore'] + '"'
    args += ' && cd && rm -rf $TMP'

    output = subprocess.check_output(['ssh', host, args], stderr=subprocess.STDOUT)

    if output:
      subject = 'WARNING : Uncommitted Changes in ' + location['repo'] + ' on ' + host
      if options.print_only:
        print subject + "\n"
        print output
      else:
        send_sns(config['sns-topic-full'], subject, output)
        send_sns(config['sns-topic-summary'], subject, subject)
