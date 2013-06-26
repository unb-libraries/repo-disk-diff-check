#!/bin/sh
temp_checkout_path=$1
repository_path=$2
deploy_path=$3

rm -rf /tmp/$temp_checkout_path
mkdir /tmp/$temp_checkout_path

git clone --recursive $repository_path $temp_checkout_path

for f in $temp_checkout_path
	for g in $deploy_path
do
	DIFF=$DIFF$(diff f g)
done

if["$DIFF" != ""]
	then
	echo "There are some differences"
	/var/opt/ec2-sns-sender/sns_send -t arn:aws:sns:us-east-1:344420214229:unb_lib_git_pushes -s '[Relentless][etc Files][PUSH]' -m "$DIFF" --subject "DIFF Files have changed"
fi
