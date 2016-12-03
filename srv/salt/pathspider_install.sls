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
    - refresh: True

#upgrade-to-testing:
#  pkg.uptodate:
#    - refresh: True
#
# I don't know why, but this package up to date stuff did not seem to really
# Work. So I just use a command now

#
# This also does not work, because the minion kills the command when upgrading itself
#upgrade-to-testing:
#  cmd.run:
#    - name: "apt-get update; DEBIAN_FRONTEND=noninteractive APT_LISTCHANGES_FRONTEND=none apt-get -o Dpkg::Options::='--force-confold' --force-yes -fuy dist-upgrade"
#

# Currently not running because the latest openssl breaks salt
#run-apt-dist-upgrade:
#  module.run:
#      - name: pkg.upgrade
#      - refresh: True
#      - dist_upgrade: True

pip-install-pathspider:
  pip.installed:
    - editable: git+git://github.com/mami-project/pathspider.git@production-piet#egg=pathspider
    - source: True
    - bin_env: /usr/bin/pip3

make-output-dir:
  file.directory:
      - name: /var/pathspider

sync-modules:
  module.run:
    - name: saltutil.sync_modules
