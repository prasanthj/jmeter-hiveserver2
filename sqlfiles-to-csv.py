import os,sys

directory = sys.argv[1]
for filename in os.listdir(directory):
	if filename.endswith(".sql"):
		queryname = os.path.basename(filename)
		with open(os.path.join(directory,filename)) as f:
			lines = f.readlines()
			# remove comments from lines, use, set commands
			nocomments = filter(lambda v: not (v.strip().startswith("--") or v.strip().lower().startswith("use") or v.strip().lower().startswith("set")), lines)
			# remove line endings
			nolinebreaks = map(lambda v: v.strip().lower(), nocomments)
			joinedquery = " ".join(nolinebreaks).strip()
			query = joinedquery.rstrip(';')
		print queryname.strip() + "^" + query
