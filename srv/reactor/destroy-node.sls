slack-message:
  slack.post_message:
    - channel: '#salt-test'
    - from_name: salty
    - message: 'A test was completed'
    - api_key: 'xoxb-92844852883-d3I6FhPi4VNfSf9VLKSO9qFG'



#destory-minion:
#  runner.cloud.destroy:
#    - instances:
#      - {{ data['id'] }}
