import subprocess
#ls -l | more
p = subprocess.Popen(["ls", "-l"], stdin = None, stdout = subprocess.PIPE)

p2 = subprocess.Popen(["sort", "-r"], stdin = p.stdout, stdout= None)
#print(p2.communicate()[0].decode())