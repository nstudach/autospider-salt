{% set task = salt['grains.get']('task', None) %}

{% if task == 'pathspider' %}
include:
  - pathspider_install
  - pathspider_run
{% endif %}
