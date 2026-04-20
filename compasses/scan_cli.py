import subprocess

res = subprocess.run(["sudo", "./cli_scan/scanner2"], capture_output=True, text=True)

print(res.stdout)