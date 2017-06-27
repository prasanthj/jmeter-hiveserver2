import xml.etree.ElementTree
import os,sys
from subprocess import call
import re, sys

NX = True
try:
	import networkx as nx
except:
	NX = False 
	sys.stderr.write("Could not import nx\npip install networkx, please\n")

try:
	import graphviz as gv
except:
	sys.stderr.write("Could not import graphviz\npip install graphviz, please\n")

def which(program):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

VALID=re.compile("([A-Za-z0-9 ]*) <-(.*)")
EDGE = re.compile("([A-Za-z0-9 ]*) \(([A-Z_]*)\)")
COLOURS =['',
'red', 'green', 'blue', 'cyan', 
'purple', 'magenta', 'pink',
'forestgreen', 'teal' 
]

def mark_cycles(edges):
	if NX:
		return _mark_cycles(edges)

def _mark_cycles(edges):
	import networkx as nx
	g = nx.DiGraph()
	for k in edges:
		for e in edges[k]:
			g.add_edge(e.src, e.target)
	cycles = sorted(list(nx.simple_cycles(g)), key=lambda a : len(a))
	for (i,c) in enumerate(cycles):
		b = c[1:]+[c[0]]
		bad = zip(c,b)
		for (x,y) in bad:
			# remember edges is target -> sources
			for z in filter(lambda a : a.src == x, edges[y]):
				z.cycle = i+1 
	return len(cycles)

class TezEdge(object):
	def __init__(self, target, (src, kind)):
		self.target = target
		self.src = src
		self.kind = kind
		self.cycle = 0 
	def __repr__(self):
		return "%s -> %s (cycle=%s)" % (self.src, self.target, self.cycle) 

def parse(l):
	m = VALID.match(l)
	if m:
		target = m.group(1)
		sources = [TezEdge(target, EDGE.match(x.strip()).groups()) for x in m.group(2).split(",")]
		return (target,sources)

def get_explain_graph(plan):
	edges = dict(filter(lambda a : a, [parse(l.strip()) for l in plan.split("\n")])) 
	label = {"BROADCAST_EDGE" : "broadcast", "CUSTOM_SIMPLE_EDGE" : "unsorted", "SIMPLE_EDGE" : "sorted", "CUSTOM_EDGE" : "bucketed"}
	n = mark_cycles(edges)

	result = "digraph {\n"
	if n:
		result +='label = "%s";labelloc="t";\n' % ("%d Cycles" % n)
	for k in edges:
		v=edges[k]
		for e in v:
			result += '"%s" -> "%s" [label="%s", color="%s"];\n' % (e.src,e.target,label.get(e.kind), COLOURS[e.cycle]) 
	result += "}\n"
	return result

is_explain_formatted = True
sysargs = len(sys.argv)
if sysargs < 3:
	print "Usage: python explain-from-jmeter.py <location-to-jmeter-summary-xml-file> <output-directory-to-store-explain-files>"
	exit()

jmeter_xml = sys.argv[1]
output_dir = sys.argv[2]
simple_lipwig = os.path.join(output_dir, "lipwig-simple")
detail_lipwig = os.path.join(output_dir, "lipwig-detail")
root = xml.etree.ElementTree.parse(jmeter_xml).getroot()

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

found_lipwig = False
if which('lipwig'):
	found_lipwig = True
	if not os.path.exists(simple_lipwig):
	    os.makedirs(simple_lipwig)

	if not os.path.exists(detail_lipwig):
	    os.makedirs(detail_lipwig)

for sample in root:
	words_with_sql = filter(lambda x: 'sql' in x, sample.get('lb').split(' '))
	query = words_with_sql[0]
	explain_filename = os.path.join(output_dir, query + "-explain.txt")
	if "[Select Statement]" in sample.find('samplerData').text:
		response = sample.find('responseData').text
		if "Explain" in response:
			explain_str = response[len("Explain"):]
			file = open(explain_filename, "w")
			file.write(explain_str.strip())
			file.close()
			if found_lipwig and is_explain_formatted:
				call(["lipwig", "-i", explain_filename, "-o", str(os.path.join(detail_lipwig, query + "-explain.svg"))])
				call(["lipwig", "-s", "-i", explain_filename, "-o", str(os.path.join(simple_lipwig, query + "-explain-simple.svg"))])
			if not is_explain_formatted:
				graph = get_explain_graph(explain_str)
				graph_svg_out = os.path.join(output_dir, query + "-explain-graph")
				dot = gv.Source(graph, format='svg')
				dot.render(graph_svg_out, cleanup=True)
				print "Explain output graph written to " + graph_svg_out + ".svg"
