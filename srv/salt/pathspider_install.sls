testing-repos:
  cmd.run:
    - name: "sed -i -- 's/jessie/testing/g' /etc/apt/sources.list"

upgrade-to-testing:
  pkg.uptodate:
    - refresh: True

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
    - fromrepo: testing
    - refresh: False

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
