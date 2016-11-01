slack-message:
  slack.post_message:
    - channel: '#minions'
    - from_name: "Minion {{grains['id']}}"
    - message: 'Pathspider measurement completed'
    - icon: 'https://devae.re/f/eth/pathspider/icons/info.png'

{% if ('when_done' in grains) and (grains['when_done'] == 'destroy') %}
request-deletion:
  event.send:
      - name: "mami/mgmt/request/destroy/{{grains['id']}}"
{% endif %}  
