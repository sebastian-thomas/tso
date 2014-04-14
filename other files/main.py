#!/usr/bin/python
import string
import sys
import ordering

import glob
from xml.dom import minidom
from document import Document
import os

def summarize(inpdir,no_of_clusters,task):
	doc = Document(ques_root_directory+inpdir,no_of_clusters)
	print "Number of Sentences :"
	print len(doc.sentences)
	#print doc.sent_no_swords
	#print len(doc.sent_no_swords)

	print "Initial cluster sentences:"

	for i in range(len(doc.clusters)):
		print doc.clusters[i][0],

	#doc.printinit_clust()


	doc.cluster_vector()
	doc.find_clust_similar_sent()
	print ""
	print "Simi based cluster sentences:"
	print doc.clust_sentences
	doc.printclust_sentences()


	print "###"
	'''

	print "weight cluster sentences:"
	doc.select_cluster_sentences()
	print doc.clust_sentences
	doc.printclust_sentences()
	'''

	'''
	print "document cluster sentences:"
	doc.clust_doc_sent()
	print doc.clust_sentences
	doc.printclust_sentences()
	'''

	#doc.printclust_sentences()
	#doc.print_rogue_clust_sentences()
	print "Ordering...."

	'''
	for input_file in inputs:
		count = count +1
	if count == 1:
		doc.print_sent_ordered()
	'''

	#ordering
	

	first = ordering.precedence_ordering(doc,doc.clust_sentences)

	tempv = doc.clust_sentences[0]
	doc.clust_sentences[0] = doc.clust_sentences[first]
	doc.clust_sentences[first] = tempv

	ordered_sentences=ordering.similarity_ordering(doc,doc.clust_sentences)
	#print doc.clust_sentences,ordered_sentences

	#****exchange 1st sentence in the cluster with first

	print ""
	print "SUMMARY of",no_of_clusters," :"

	for i in ordered_sentences:
		print doc.sentences[i],". "
	



	#doc.print_rogue_clust_sentences()
	print("writing op of task "+str(task))
	doc.write_rogue_clust_sentences(sys_dir,task)

	#print "Ordering...."
	#doc.print_sent_ordered()



def main():
	

	ques_dir = []
	res_dir = []

	no_of_clusters = int(sys.argv[1])

	dirs =  [x[0] for x in os.walk(ques_root_directory)]
	i = 0
	for d in dirs:
		d = d.split('/')
		t_dir = d[len(d)-1]
		if(len(t_dir)>1):
			ques_dir.append(d[len(d)-1])
			i = i +1

		#to work with few sets
		if i == 10:
			break

	#print ques_dir

	dirs =  [x[0] for x in os.walk(res_root_directory)]
	for d in dirs:
		d = d.split('/')
		t_dir = d[len(d)-1]
		if(len(t_dir)>1):
			res_dir.append(d[len(d)-1])

	#print res_dir

	task = 0;

	

	for d in ques_dir:		
		task = task + 1
		print d,task
		f_settings = open(settings_file+str(task)+".xml",'w')
		f_settings.write('<ROUGE_EVAL version="1.55">\n')
		f_settings.write('\t<EVAL ID="'+str(task)+'">\n')
		f_settings.write('\t\t<MODEL-ROOT>/home/seb/proj/obj/eval/models</MODEL-ROOT>\n')
		f_settings.write('\t\t<PEER-ROOT>/home/seb/proj/obj/eval/systems</PEER-ROOT>\n')
		f_settings.write('\t\t<INPUT-FORMAT TYPE="SEE"></INPUT-FORMAT>\n')
		f_settings.write('\t\t<PEERS>\n')
		f_settings.write('\t\t\t<P ID="1">'+str(task)+'.html</P>\n')
		f_settings.write('\t\t</PEERS>\n')
		f_settings.write('\t\t<MODELS>\n')
		f_settings.write('\t\t\t<M ID="1">'+str(task)+'.html</M>\n')
		f_settings.write('\t\t</MODELS>\n')
		f_settings.write('\t</EVAL>\n')

		

		summarize(d,no_of_clusters,task)

		#now make summaries in ROUGE understandable form

		for d2 in res_dir:
			if d in d2:
				format_result(d2,task)
				break #takes only one evaluation
		

		f_settings.write('</ROUGE_EVAL>\n')



def format_result(d2,task):
	f1 = res_root_directory+d2+'/200e' #considering 200e files
	xmldoc = minidom.parse(f1)
	itemlist = xmldoc.getElementsByTagName("s")
	f2 = open(models_dir+str(task)+'.html','w')

	f2.write("<html>\n")
	f2.write("<head><title>"+str(task)+".html</title> </head>\n")
	f2.write('<body bgcolor="white">\n')

	i = 1

	for sent in itemlist:
		#print sent.firstChild.data
		f2.write('<a name="')
		f2.write(str(i))
		f2.write('">[')
		f2.write(str(i))
		f2.write(']</a> <a href="#')
		f2.write(str(i))
		f2.write('" id=')
		f2.write(str(i))
		f2.write('>')
		f2.write(sent.firstChild.data.rstrip())
		f2.write('. </a>\n')
		i = i + 1
	f2.write("</body>\n")
	f2.write( "</html>\n")
	
if __name__ == "__main__":
	inpdir = "/home/seb/proj/obj/duc02.results.data/data/test/docs.with.sentence.breaks/d061j/*.S"
	ques_root_directory = 'duc02.results.data/data/test/docs.with.sentence.breaks/'
	res_root_directory = 'duc02.results.data/data/test/summaries/duc2002extracts/'

	settings_file = 'eval/settings'
	models_dir = 'eval/models/'
	sys_dir = 'eval/systems/'

	main()
