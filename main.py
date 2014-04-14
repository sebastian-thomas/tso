#!/usr/bin/python
import string
import ordering
import sys
from document import Document

def main():
	#inputs = ['ip1.txt','ip2.txt']
	#inputs = ['ip3.txt','ip4.txt']
	#inputs = ['sachin1.txt']
	#inputs = ['mal1.txt']
	inputs = ['ip5.txt','ip6.txt','ip7.txt']
	no_of_clusters = int(sys.argv[1])
	doc = Document(inputs,no_of_clusters)
	count = 0
	print "Number of Sentences :"
	print len(doc.sentences)
	#print doc.sent_no_swords
	#print len(doc.sent_no_swords)
	'''

	print "Initial cluster sentences:"

	for i in range(len(doc.clusters)):
		print doc.clusters[i][0],
	'''	

	print "Selecting sentence from each cluster..."
	doc.cluster_vector()
	doc.find_clust_similar_sent()
	#print ""
	#print "Cluster sentences:\n"
	#print doc.clust_sentences

	#print "Assigning weights to cluster sentences:"
	#doc.select_cluster_sentences()

	

	#doc.printclust_sentences()
	#doc.print_rogue_clust_sentences()
	print "Ordering...."
	for input_file in inputs:
		count = count +1
	if count == 1:
		doc.print_sent_ordered()

	#ordering
	

	first = ordering.precedence_ordering(doc,doc.clust_sentences)

	tempv = doc.clust_sentences[0]
	doc.clust_sentences[0] = doc.clust_sentences[first]
	doc.clust_sentences[first] = tempv

	ordered_sentences=ordering.similarity_ordering(doc,doc.clust_sentences)
	#print doc.clust_sentences,ordered_sentences

	#****exchange 1st sentence in the cluster with first


	for i in ordered_sentences:
		print doc.sentences[i].lstrip().capitalize(),". ",

if __name__ == "__main__":
	main()
