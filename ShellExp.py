import subprocess
import os
import signal
import sys
import shlex

#f(x) | g(x) | s(x)
#pwd | python bah.py
def fshloop():
	BuiltinCmds = ['cd','pwd', 'jobs', 'bg', 'fg', 'exit']
	done = False
	while(not done):
		
		
		#get input from user 
		UserCmd = input("fsh$")
		


		#split it into a bunch of smaller commands based on wether it is piped 
		UserCmd = UserCmd.split(" | ")
		UserCmdLen = len(UserCmd) 
		#run each command and give its output to the next process
		PipedStdout = None
		
		for i in range(0, UserCmdLen):
			UserCmd[i] = UserCmd[i].split()
			#if command is a builtin
			if UserCmd[i][0] in BuiltinCmds:
				#run builtin function	
				p = FshBuiltins(UserCmd[i])
				PipedStdout = p.stdout
			elif i == UserCmdLen - 1:
				#run execute function
				#ls -l | sort -r
				p = subprocess.Popen(UserCmd[i], stdin = PipedStdout)
				PipedStdout = p.stdout
			else:
				p = subprocess.Popen(UserCmd[i], stdin = PipedStdout, stdout = subprocess.PIPE )
				PipedStdout = p.stdout
				#if p!= None:
					#out, error = p.communicate()
					#print("yes")
					#if error == None:
						#print(out.decode())

					#else:
						#print("Something broke!", str(error)) 
	return
	
def FshBuiltins(UserCmd):
	if UserCmd[0] == 'exit':
		print("Exiting...")
		sys.exit(0)

	if UserCmd[0] == "cd":
		try:
			os.chdir(UserCmd[1])
		except Exception:
			print("Nope:, ", Exception)
		print(os.getcwd())
		return os.getcwd()	 

	if UserCmd[0] == 'pwd':
		print(os.getcwd())
		return os.getcwd()

	if UserCmd[0] == 'jobs':
		return

	if UserCmd[0] == 'bg':
		return

	if UserCmd[0] == 'fg':
		return

fshloop()

