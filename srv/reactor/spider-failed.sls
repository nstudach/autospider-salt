notify-slack:
  local.slack.post_message:
    - tgt: {{ data['id'] }}
    - arg:
      - channel=#minions
      - from_name="Minion {{ data['id']}}"
      - message='pietdv, Pathspider measurement FAILED.'
      - icon='https://devae.re/f/eth/pathspider/icons/warning.jpg'
