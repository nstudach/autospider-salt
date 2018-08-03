# Sleeping is needed because the spider started state is fired slightly before
# the installation of salt-minion is completed, and that screws up things.
sleep-for-a-bit:
  cmd.run:
    - name: sleep 120

#testing-repos:
#  cmd.run:
#    - name: "sed -i -- 's/jessie/testing/g' /etc/apt/sources.list"

# Getting a completely new sources.list file. Doing this becuase I had problems
# with the digitalocean mirrors. I opted to use the nl repos, because I assume
# that they are hosted somewhere nice and close to amsix

get-sources-file:
  file.managed:
    - name: /etc/apt/sources.list
    - source: salt://sources.list

refresh-packet-list:
  cmd.run:
    - name: "apt-get update"

apt-install:
  pkg.installed:
    - pkgs:
      - python3-libtrace
      - python3-sphinx
      - python3-straight.plugin
      - python3-setuptools
      - pylint3
      - python3-pep8
      - python3-dev
      - python3-dnspython
      - python3-pip
      - python3-requests
      - python-pip
      - git
      - python3-straight.plugin
      - python3-pyroute2
      - python3-scapy-python3
      - python3-stem
      - python3-dnslib
      - python3-pycurl
      - python3-nose
    - refresh: True

pip-install-pathspider:
  pip.installed:
    - editable: git+git://github.com/nstudach/pathspider.git@uploader#egg=pathspider
    - source: True
    - bin_env: /usr/bin/pip3

make-output-dir:
  file.directory:
      - name: /var/pathspider

sync-modules:
  module.run:
    - name: saltutil.sync_modules
