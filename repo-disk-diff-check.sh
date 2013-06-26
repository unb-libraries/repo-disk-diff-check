#!/bin/sh
temp_checkout_path="/tmp/$$"
repository_path=$1
deploy_path=$2
sns_topic_id=$3
server_id=$4
short_message=$5

rm -rf $temp_checkout_path
mkdir $temp_checkout_path
git clone --recursive $repository_path $temp_checkout_path

temp_checkout_files=$(find $temp_checkout_path -type f | grep -v '\/\.git\/')
for checked_out_file in $temp_checkout_files; do
        deployed_file=$(echo $checked_out_file | sed -e 's|'$temp_checkout_path'|'$deploy_path'|g')
        deployed_diff=$(diff $checked_out_file $deployed_file | sed -e 's/^\s*//g' -e 's/(\s|\n)*$//g' )
        if [ "$deployed_diff" ]
        then
                relative_filepath=$(echo $checked_out_file | sed -e 's|'$temp_checkout_path'/||g')
                output_block="$output_block
$4 : $1
$relative_filepath
$deployed_diff
"
        fi
done

rm -rf $temp_checkout_path

if [ "$output_block" ]
then
	if [ "$short_message" ]
	then
	/var/opt/ec2-sns-sender/sns_send -t $3 -s "Uncommitted Changes in $1 on $4" -m "WARNING : Uncommitted Changes in $1 on $4"
	else
	/var/opt/ec2-sns-sender/sns_send -t $3 -s "Uncommitted Changes in $1 on $4" -m "$output_block"
	fi
fi
