{% set task = salt['grains.get']('task', None) %}
{% set state = salt['grains.get']('task-state', None) %}

{% if task == 'pathspider' %}
#{% if state == None %}

include:
  - pathspider_install
  - pathspider_run

set-ps-installed-grain:
  grains.present:
    - name: task-state
    - value: pathspider-installed
    - force: True


#reboot-minion:
#  module.run:
#    - name: system.reboot
#
#{% elif state == 'pathspider-installed' %}
#

#include:
#  - pathspider_run

#{% endif %}
{% endif %}
