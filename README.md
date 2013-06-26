relentless-repo-diff-check
==========================
Notify via SNS if a difference exists between a bare git repository that is deployed to disk and actual disk contents

Usage: ./repo-diff-check.sh $1 $2 $3 $5 ($5)

$1 : Path to the bare repository
$2 : Path to the point on the disk the repository is checked out to
$3 : SNS topic to notify in case of changes
$4 : A server ID string used in building the SNS messages
$5 : (Optional) short message switch "True" to only notify of changes, not detail them in the SNS notification
