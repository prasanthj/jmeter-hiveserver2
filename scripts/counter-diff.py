import os, sys, zipfile, json
from texttable import Texttable

TEZ_DAG = "TEZ_DAG"

def diff(file1, file2):
	# extract ZIP files
	file1_dir = os.path.splitext(file1)[0]
	file2_dir = os.path.splitext(file2)[0]
	if not os.path.exists(file1_dir):
		os.makedirs(file1_dir)
	if not os.path.exists(file2_dir):
		os.makedirs(file2_dir)

	zip_ref = zipfile.ZipFile(os.path.abspath(file1), 'r')
	zip_ref.extractall(os.path.abspath(file1_dir))
	zip_ref.close()

	zip_ref = zipfile.ZipFile(os.path.abspath(file2), 'r')
	zip_ref.extractall(os.path.abspath(file2_dir))
	zip_ref.close()

	# Read TEZ_DAG file as json
	file1_dag = os.path.join(os.path.abspath(file1_dir), TEZ_DAG)
	file2_dag = os.path.join(os.path.abspath(file2_dir), TEZ_DAG)

	# populate diff table
	difftable = {}
	with open(file1_dag) as data_file:
		file1_dag_json = json.load(data_file)
		counters = file1_dag_json['otherinfo']['counters']
		for group in counters['counterGroups']:
			countertable = {}
			for counter in group['counters']:
				counterName = counter['counterName']
				countertable[counterName] = []
				countertable[counterName].append(counter['counterValue'])

			groupName = group['counterGroupName']
			difftable[groupName] = countertable

	with open(file2_dag) as data_file:
		file2_dag_json = json.load(data_file)
		counters = file2_dag_json['otherinfo']['counters']
		for group in counters['counterGroups']:
			groupName = group['counterGroupName']
			countertable = difftable[groupName]
			for counter in group['counters']:
				counterName = counter['counterName']
				# if counter does not exist in file1, add it with 0 value
				if counterName not in countertable:
					countertable[counterName] = [0]
				countertable[counterName].append(counter['counterValue'])

	# if some counters are missing, consider it as 0 and compute delta difference
	for k,v in difftable.items():
		for key, value in v.items():
			# if counter value does not exisit in file2, add it with 0 value
			if len(value) == 1:
				value.append(0)

			# store delta difference
			value.append(value[0] - value[1])

	return difftable

def print_table(difftable, name1, name2):
	table = Texttable(max_width=0)
	table.set_cols_align(["l", "l", "l", "l", "l"])
	table.set_cols_valign(["m", "m", "m", "m", "m"])
	table.add_row(["Counter Group", "Counter Name", name1, name2, "delta"]);
	for k,v in difftable.items():
		row = []
		# counter group
		row.append(k)

		# keys as list (counter names)
		row.append("\n".join(list(v.keys())))

		# counter values for dag1
		for key, value in v.items():
			if len(value) == 1:
				value.append(0)
			value.append(value[0] - value[1])

		# dag1 counter values
		name1Val = []
		for key, value in v.items():
			name1Val.append(str(value[0]))
		row.append("\n".join(name1Val))

		# dag2 counter values
		name2Val = []
		for key, value in v.items():
			name2Val.append(str(value[1]))
		row.append("\n".join(name2Val))

		# delta values
		deltaVal = []
		for key, value in v.items():
			deltaVal.append(str(value[2]))
		row.append("\n".join(deltaVal))

		table.add_row(row)

	print table.draw() + "\n"

sysargs = len(sys.argv)
if sysargs < 3:
	print "Usage: python diff.py dag_file1.zip dag_file2.zip"
	exit()

file1 = sys.argv[1]
file2 = sys.argv[2]
difftable = diff(file1, file2)
print_table(difftable, os.path.splitext(file1)[0], os.path.splitext(file2)[0])