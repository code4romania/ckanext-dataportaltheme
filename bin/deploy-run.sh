ssh -i bin/deploy.pem -o "StrictHostKeyChecking no" deploy@$AWS_MACHINE
cd scripts
. stop_dataportal.sh
. start_dataportal.sh
exit