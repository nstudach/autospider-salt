destory-minion:
  runner.cloud.destroy:
    - instances:
      - {{ data['id'] }}
