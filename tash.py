import sys
import os
import subprocess

PROMPT = "$ "
EXIT = "exit"
CD = "cd"
PWD = "pwd"
JOBS = "jobs"
BG = "bg"
FG = "fg"
PIPE = " | "

BUILTINS = [CD, PWD, JOBS, BG, FG, EXIT]

def tash_cd(file_path):
	try:
		os.chdir(file_path)
	except Exception as e:
		print("something went wrong :( there's probably no filepath. exception: ", e)

# executes the given command
def exc(uinput):
	try:
		commands = uinput.split(PIPE)
		#run each command and give its output to the next process
		PipedStdout = None
		num_commands = len(commands)
		for i in range(0, num_commands):
			commands[i] = commands[i].split()
			#if command is a builtin
			if commands[i][0] in BUILTINS:
				#run builtin function	
				p = builtins(commands[i])
			elif i == num_commands-1:
				#run execute function
				p = subprocess.Popen(commands[i], stdin = PipedStdout).wait()
			else:
				p = subprocess.Popen(commands[i], stdin = PipedStdout, stdout = subprocess.PIPE)
				PipedStdout = p.stdout
	except Exception as e:
		print("something went wrong :( there's probably no such command. exception: ", e)
	return 0

# loop to ask for user input
def tash_loop():
	while True:
		done = False
		while not done:
			uin = input(PROMPT)
			if len(uin) != 0:
				done = True
		
		# if uin == EXIT:
		# 	return 0
		# # cd command (builtin)
		# if uin[:len(CD)] == CD:
		# 	# filepath
		# 	fp = uin[len(CD):]
		# 	tash_cd(fp)
		# else:
		# 	exc(uin)
		exc(uin)

def builtins(UserCmd):
	if UserCmd[0] == EXIT:
		print("Exiting...")
		sys.exit(0)
		return

	if UserCmd[0] == "cd":
		try:
			os.chdir(UserCmd[1])
		except Exception:
			print("Nope:, ", Exception)
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


def main():
	tash_loop()
	return

main()