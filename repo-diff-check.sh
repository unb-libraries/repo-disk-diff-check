#!/bin/sh
# repo-diff-check /tmp/relentless-etc-compare-files/etc /var/opt/repos/relentless-etc-files
#tmp_to_check= "/tmp/relentless-etc-compare-files/etc"
#file-from-etc ="/var/opt/repos/relentless-etc-files"
tmp_to_check = $1
file-from-etc = $2
rm -rf /tmp/$tmp_to_check
mkdir /tmp/$tmp_to_check
git clone --recursive $file-from-etc $tmp_to_check
for f in $tmp_to_check
	for g in $file-from-etc
do
	DIFF = $DIFF$(diff f g)
done

if["$DIFF" != ""]
	then
	echo "There are some differences"
	/var/opt/ec2-sns-sender/sns_send -t arn:aws:sns:us-east-1:344420214229:unb_lib_git_pushes -s '[Relentless][etc Files][PUSH]' -m "$DIFF" --subject "DIFF Files have changed"
fi
