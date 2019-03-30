ssh -i deploy.pem deploy@$AWS_MACHINE
cd scripts
. stop_dataportal.sh
. start_dataportal
exit