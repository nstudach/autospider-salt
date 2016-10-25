notify-slack:
  local.slack.post_message:
    - tgt: {{ data['id'] }}
    - arg:
      - channel=#minions
      - from_name="Minion {{ data['id']}}"
      - message='Pathspider measurement completed.'
      - icon='https://devae.re/f/eth/pathspider/icons/info.png'

#start-new-run:
#  local.state.apply:
#    - tgt: {{ data['id'] }}
#    - arg:
#      - pathspider-install-and-run
