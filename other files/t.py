import glob
from xml.dom import minidom
import sys

print "<html>"
print "<head><title>filename_here</title> </head>"
print '<body bgcolor="white">'

i = 1;

files =  glob.glob("/home/seb/proj/obj/duc02.results.data/data/test/summaries/duc2002extracts/d061jb/200e")
for f in files:
	xmldoc = minidom.parse(f)
	itemlist = xmldoc.getElementsByTagName("s")
	for sent in itemlist:
		#print sent.firstChild.data
		sys.stdout.write('<a name="')
		sys.stdout.write(str(i))
		sys.stdout.write('">[')
		sys.stdout.write(str(i))
		sys.stdout.write(']</a> <a href="#')
		sys.stdout.write(str(i))
		sys.stdout.write('" id=')
		sys.stdout.write(str(i))
		sys.stdout.write('>')
		sys.stdout.write(sent.firstChild.data)
		sys.stdout.write('. </a>')
		print ""
		i = i + 1
print "</body>"
print "</html>"