import os,sys,errno

inputDir = os.path.abspath(sys.argv[1])
outputDir = os.path.abspath(sys.argv[2])
if not os.path.exists(outputDir):
    try:
        os.makedirs(outputDir)
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

for filename in os.listdir(inputDir):
	if filename.endswith(".sql"):
		queryname = os.path.basename(filename)
		outFile = os.path.abspath(os.path.join(os.path.abspath(outputDir), os.path.splitext(filename)[0] + ".csv"))
		with open(os.path.join(inputDir,filename)) as f:
			lines = f.readlines()
			# remove comments from lines, use, set commands
			nocomments = filter(lambda v: not (v.strip().startswith("--") or v.strip().lower().startswith("use") or v.strip().lower().startswith("set")), lines)
			# remove line endings
			nolinebreaks = map(lambda v: v.strip(), nocomments)
			joinedquery = " ".join(nolinebreaks).strip()
			query = joinedquery.rstrip(';')

		file = open(outFile,"w+")
		frags = []
		if ";" in query:
			frags = query.split(";")
		else:
			file.write(queryname.strip() + "^" + query)

		for i, frag in enumerate(frags):
			file.write(queryname.strip() + "_" + str(i) + "^" + frag.strip() + "\n")

		file.close()
		print "Output written to " + outFile
