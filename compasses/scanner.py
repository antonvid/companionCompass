import subprocess

def execute(cmd):
    scanner = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    grep = subprocess.Popen(['grep', '28:CD:C1:0F:BE:9A'], stdin=scanner.stdout, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(grep.stdout.readline, ""):
        yield stdout_line
        print('yield')
    grep.stdout.close()
    return_code = grep.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

for path in execute(["sudo", "./scanner"]):
    print(path, end="")
