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
GOODBYE = "My battery is low and it's getting dark..."

BUILTINS = [CD, PWD, JOBS, BG, FG, EXIT]

def tash_cd(file_path):
	try:
		os.chdir(file_path)
	except Exception as e:
		print("something went wrong :( there's probably no filepath. exception: ", e)
	return os.getcwd()

# executes the given command
def exc(uinput):
	try:
		commands = uinput.split(PIPE)
		#run each command and give its output to the next process
		prev_out = None
		num_commands = len(commands)
		for i in range(0, num_commands):
			commands[i] = commands[i].split()
			#if command is a builtin
			if commands[i][0] in BUILTINS:
				#run builtin function	
				p = builtins(commands[i])
			elif i == num_commands-1:
				#run execute function
				p = subprocess.Popen(commands[i], stdin = prev_out).wait()
			else:
				p = subprocess.Popen(commands[i], stdin = prev_out, stdout = subprocess.PIPE)
				prev_out = p.stdout
	except Exception as e:
		print("something went wrong :( there's probably no such command. exception: ", e)
	return 0

# loop to ask for user input
def tash_loop():
	while True:
		good_uin = False
		while not good_uin:
			uin = input(PROMPT)
			if len(uin) != 0:
				good_uin = True
		exc(uin)

def builtins(uinput):
	if uinput[0] == EXIT:
		print(GOODBYE)
		sys.exit(0)
		return

	if uinput[0] == CD:
		return tash_cd(uinput[1])

	if uinput[0] == PWD:
		print(os.getcwd())
		return os.getcwd()

	if uinput[0] == 'jobs':
		return

	if uinput[0] == 'bg':
		return

	if uinput[0] == 'fg':
		return


def main():
	tash_loop()
	return

main()