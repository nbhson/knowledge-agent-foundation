# Agent gọi script thay vì generate tokens
import subprocess, json

result = subprocess.run(
    ["python", "scripts/run_static_analysis.py", "--path", "./src"],
    capture_output=True, text=True, timeout=60
)
report = json.loads(result.stdout)
