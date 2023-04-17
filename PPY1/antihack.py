import bleach
def scan(arg):
	for i in arg:
		if "drop table" in str(i.lower()) or "drop database" in str(i.lower()):
			log('sql injection attempt')
			return False
	return True
def clean(arg):
	if type(arg)==str:
		return (bleach.clean(arg))
	else:
		return(arg)
def log(data):
	f= open("logFile.txt","a")
	stat=data
	f.write("{}".format(stat))
	f.write("\n")
	f.close
