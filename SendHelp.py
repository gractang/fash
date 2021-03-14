import subprocess
#ls -l | sort -r
p = subprocess.Popen(["ls", "-l"], stdin = None, stdout = subprocess.PIPE)
p2 = subprocess.Popen(["sort", "-r"], stdin = p.stdout, stdout = subprocess.PIPE)
print(p2.communicate()[0])