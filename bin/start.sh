set -e

if [[ "$*" != "fast" ]]
then
  vagrant destroy -f
fi

vagrant up || vagrant reload && vagrant up
vagrant ssh -c "source /usr/lib/ckan/default/bin/activate; paster serve /etc/ckan/default/development.ini --reload"
