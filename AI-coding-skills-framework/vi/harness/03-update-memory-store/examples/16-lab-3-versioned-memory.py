# python 03-update-memory-store/lab_versioned.py

vm = VersionedMemory()

# Track evolving knowledge
vm.set("bhyt_rate", "4.5%", message="Initial fact")
vm.set("bhyt_rate", "4.5% lương cơ sở", message="More specific")
vm.set("bhyt_rate", "4.5% MEC 2024", message="Updated year")

# View history
for entry in vm.log():
    print(f"  v{entry['id']}: {entry['message']}")

# Compare versions
diff = vm.diff(0, 2)
print(f"Changes: {diff['count']}")

# Rollback
state = vm.rollback(0)
print(f"Rolled back to: {state['rolled_back_to']}")
