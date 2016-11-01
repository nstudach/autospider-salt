#notify-slack:
#  local.slack.post_message:
#    - tgt: {{ data['id'] }}
#    - arg:
#      - channel=#minions
#      - from_name="Minion {{ data['id']}}"
#      - message='Pathspider measurement completed.'
#      - icon='https://devae.re/f/eth/pathspider/icons/info.png'

run-state-file:
  local.state.apply:
    - tgt: {{ data['id'] }}
    - arg:
      - spider_completed_state
