{% set inputfile = salt['grains.get']('web', 'default') %}

get-input-file:
  file.managed:
    - name: /tmp/pathspider_in.csv
    - source: salt://pathspider_inputs/{{inputfile}}.csv

run-pathspider:
  module.run:
    - name: pathspider.run
    - inputfile: /tmp/pathspider_in.csv
