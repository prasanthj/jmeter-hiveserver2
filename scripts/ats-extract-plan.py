import json
import os,sys

class ATSFile(object):
	def __init__(self, name):
		self.data = json.load(open(name))
		self.name = name
	def dump(self):
		if "hive_query_id" in self.data:
			info = self.data["hive_query_id"]["otherinfo"]
		else:
			info = self.data["otherinfo"]
		q = json.loads(info["QUERY"])
		txt = q["queryText"]
		plan = q["queryPlan"]
		queryFile = self.name + "-query.txt"
		planFile = self.name + "-plan.txt"
		open(queryFile, "w").write(txt)
		json.dump(plan, open(planFile,"w"), indent=2)
		print ("Query written to " + os.path.abspath(queryFile))
		print ("Query plan written to " + os.path.abspath(planFile))
def main(args):
	data = [ATSFile(f) for f in args]
	for d in data:
		d.dump()

if __name__ == "__main__":
	main(sys.argv[1:])