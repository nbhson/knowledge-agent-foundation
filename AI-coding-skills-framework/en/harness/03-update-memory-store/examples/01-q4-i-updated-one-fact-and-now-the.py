vm.set("hi_rate", "4.5% MEC 2024", message="Updated year")
vm.log()          # v0, v1, v2 with message + timestamp
vm.diff(0, 2)     # {'changes': [...], 'count': 1}
vm.rollback(0)    # {'rolled_back_to': 0, 'current_state': {...}}
