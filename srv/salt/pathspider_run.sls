{% set inputfile = salt['grains.get']('web', 'default') %}

disable-tcp-ecn-fallback:
  cmd.run:
    - name: "echo 0 > /proc/sys/net/ipv4/tcp_ecn_fallback"

get-input-file:
  file.managed:
    - name: /tmp/pathspider_in.ndjson
    - source: salt://pathspider_inputs/{{inputfile}}.ndjson

run-pathspider:
  module.run:
    - name: pathspider.run
    - inputfile: /tmp/pathspider_in.ndjson
