import sys
import os
import subprocess
PROMPT = "$ "
EXIT = "exit"
CD = "cd "
PIPE = "|"

def tash_cd(file_path):
	try:
		os.chdir(file_path)
	except Exception as e:
		print("something went wrong :( there's probably no filepath. exception: ", e)

# def tash_pipe(uinput):
# 	commands = uinput.split(PIPE)
# 	print(commands)

# executes the given command
def exc(uinput):
	uargs = uinput.split()
	# this hasn't been implemented yet btw
	# if PIPE in uinput:
	#  	tash_pipe(uinput)
	try:
		# finishes child process before starting new
		subprocess.Popen(uinput, shell=True).wait()
	except Exception as e:
		print("something went wrong :( there's probably no such command. exception: ", e)
	return 0

# loop to ask for user input
def tash_loop():
	while True:
		uin = input(PROMPT)
		if uin == EXIT:
			return 0
		# cd command (builtin)
		if uin[:len(CD)] == CD:
			# filepath
			fp = uin[len(CD):]
			tash_cd(fp)
		else:
			exc(uin)

def main():
	tash_loop()
	return

main()