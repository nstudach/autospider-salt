start-command run:
  local.state.apply:
    - tgt: {{ data['id'] }}
    - arg:
      - minion_started_state
    - kwarg:
        queue: True
