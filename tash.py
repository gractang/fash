import sys, os
PROMPT = "$ "
EXIT = "exit"
CD = "cd "

def tash_cd(file_path):
	try:
		os.chdir(file_path)
	except Exception as e:
		print("something went wrong :( exception: ", e)

# executes the given command
def exc(command):
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
		exc(uin)

def main():
	print(len(CD))
	tash_loop()
	return

main()