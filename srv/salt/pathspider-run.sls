{% set inputfile = salt['grains.get']('campaign', 'default') %}

get-input-file:
  file.managed:
    - name: /tmp/pathspider-in.csv
    - source: salt://pathspider-inputs/{{inputfile}}.csv

make-output-dir:
  file.directory:
    - name: /var/pathspider

run-pathspider:
  module.run:
    - name: pathspider.run
    - inputfile: /tmp/pathspider-in.csv
