#notify-slack:
#  local.slack.post_message:
#    - tgt: {{ data['id'] }}
#    - arg:
#      - channel=#minions
#      - from_name="Minion {{ data['id']}}"
#      - message='Pathspider measurement completed.'
#      - icon='https://devae.re/f/eth/pathspider/icons/info.png'

send-email:
  local.cmd.run:
    - tgt: master-minion
    - arg:
      - 'sendmail piet@devae.re < /srv/salt/failmail.txt'

run-state-file:
  local.state.apply:
    - tgt: {{ data['id'] }}
    - arg:
      - spider_failed_state
