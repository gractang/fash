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
HISTORY = "prev"
HIST_FILENAME = "history.txt"
PIPE = " | "
GOODBYE = "My battery is low and it's getting dark..."

BUILTINS = [CD, PWD, JOBS, BG, FG, HISTORY, EXIT]

def tash_cd(file_path):
	try:
		os.chdir(file_path)
	except Exception as e:
		print("something went wrong :( there's probably no filepath. exception: ", e)
	return os.getcwd()

def tash_prev():
	with open(HIST_FILENAME) as f:
		for line in f:
			pass
	return line

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
	f = open(HIST_FILENAME, 'w').close()
	while True:
		# check to make sure that user input is not blank
		good_uin = False
		while not good_uin:
			uin = input(PROMPT)
			if len(uin) != 0:
				good_uin = True
		f = open(HIST_FILENAME, 'a')
		f.write(uin)
		f.write("\n")
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

	# i want to do the thing where the up arrow triggers
	# but too lazy to figure out how to implement
	if uinput[0] == HISTORY:
		prev = tash_prev()
		print(prev)
		return prev


def main():
	tash_loop()
	return

main()