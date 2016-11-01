slack-message:
  slack.post_message:
    - channel: '#minions'
    - from_name: "Minion {{grains['id']}}"
    - message: 'Pathspider measurement FAILED'
    - icon: 'https://devae.re/f/eth/pathspider/icons/warning.jpg'
