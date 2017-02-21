slack-message:
  slack.post_message:
    - channel: '#minions'
    - from_name: "Minion {{grains['id']}}"
    - message: 'Pathspider measurement started'
    - icon: 'https://devae.re/f/eth/pathspider/icons/start.png'
