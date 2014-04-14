#!/usr/bin/python

import preprocessing
import helper
import cluster
import operator
import sys

class Document:
	"the class to represent all input documents"


	def __init__(self,docs,num_clu):
		self.no_clusters = num_clu
		print "Loading Sentences..."
		self.sentences =  preprocessing.load_sentences(docs)
		print "Preprocessing..."
		self.sent_no_swords = preprocessing.remove_stopwords(self.sentences)
		self.unique_terms = helper.uniqueterms(self.sent_no_swords)
		self.sent_weight = helper.tfisf(self.sent_no_swords,self.unique_terms)
		#self.sent_weight = helper.word_vector(self.sent_no_swords,self.unique_terms)
		print "Finding Similarity Graph..."
		self.sent_similarity = helper.similarity(self.sent_weight,self.sent_weight)
		print "Clustering..."
		self.clusters = cluster.kmedoid(self.sent_similarity,self.no_clusters)
		'''
		print "clustered"
		for i in range(len(self.clusters)):
			print self.sentences[i][0]
			print ""
		'''
		#print self.sentences
		#print "Medoid clusters :"
		#print self.clusters


	def clust_doc_sent(self):
		fc = []
		for clust in self.clusters:
			maxv = 0;
			maxi = 0
			for sent in clust:
				if sent !=(len(self.sent_similarity)-1) and (self.sent_similarity[len(self.sent_similarity)-1][sent] > maxv):
					maxi = sent
			fc.append(maxi)
		self.clust_sentences = fc


	def select_cluster_sentences(self):
		fc = []
		for clust in self.clusters:
			sent_weight_sum = []
			sent_edgewt_neighbours = []
			sent_inv_nowords = []

			total_wt = {}

			for sent in clust:
				#sum of tf-isf value of terms in sentence
				wt = 0.0
				#print self.sent_weight[sent]
				for q,w in self.sent_weight[sent].iteritems():
					wt = wt + float(w)
				sent_weight_sum.append(wt)

				#sum of weight of edges from each node in sentence similarity matrix
				wt = 0.0
				for sent2 in clust:
					wt = wt + self.sent_similarity[sent][sent2]
				sent_edgewt_neighbours.append(wt)

				#inversily proportional to number of sentences as summary should contain small sentences 
				wt = 0.0
				wt = 1/len(self.sent_no_swords[sent].split())
				sent_inv_nowords.append(wt)

			for i in range(len(clust)):
				val = 0.2*sent_weight_sum[i] + 0.7*sent_edgewt_neighbours[i] + 0.1*sent_inv_nowords[i]
				total_wt[clust[i]]= val

			max_value = max(total_wt.itervalues())
			t_sent = [key for key, value in total_wt.iteritems() if value == max_value]
			print t_sent,max_value
			fc.append(t_sent[0])

		self.clust_sentences = fc

	def cluster_vector(self):
		#to find the vector represntation of cluster
		clust_words = []
		for clust in self.clusters:
			allwords = ' '.join([self.sent_no_swords[ind] for ind in clust])
			clust_words.append(allwords)
		#print "Cluster Words"
		#print clust_words
		self.clust_as_sent = clust_words
		self.clust_weight = helper.tfisf(self.clust_as_sent)
		#print "Cluster Weight"
		#print self.clust_weight

	def find_clust_similar_sent(self):
		#to find out the sentence most similar to the cluster
		clust_sent_sim = helper.similarity(self.clust_weight,self.sent_weight)
		#print clust_sent_sim
		clust_sent = []
		for sim in clust_sent_sim:
			#max_val = max(sim)
			max_index = max(sim.iteritems(), key=operator.itemgetter(1))[0]
			if max_index not in clust_sent:
				clust_sent.append(max_index)
		#print "Sentence most similar to clusters..."
		#print clust_sent
		self.clust_sentences = clust_sent	

	def printclust_sentences(self):
		for i in self.clust_sentences:
			print self.sentences[i]		

		print""

	def print_rogue_clust_sentences(self):
		print "<html>"
		print "<head><title>filename_here</title> </head>"
		print '<body bgcolor="white">'

		i = 1;

		for k in self.clust_sentences:
			#print '<a name="',i,'">[',i,']</a> <a href="#',i,'" id=',i,'>',self.sentences[i],'. </a>'
			sys.stdout.write('<a name="')
			sys.stdout.write(str(i))
			sys.stdout.write('">[')
			sys.stdout.write(str(i))
			sys.stdout.write(']</a> <a href="#')
			sys.stdout.write(str(i))
			sys.stdout.write('" id=')
			sys.stdout.write(str(i))
			sys.stdout.write('>')
			sys.stdout.write(self.sentences[k])
			sys.stdout.write('. </a>')
			print ""
			i = i + 1

		print "</body>"
		print "</html>"	


	def write_rogue_clust_sentences(self,sys_dir,task):
		f = open(sys_dir+str(task)+'.html','w')
		f.write("<html>\n")
		f.write("<head><title>"+str(task)+".html</title> </head>\n")
		f.write('<body bgcolor="white">\n')

		i = 1;

		#to find wrt to cluster similarity
		for k in self.clust_sentences:
		#to find op wrt to medoid
		#for k in range(len(self.clusters)):
			#print '<a name="',i,'">[',i,']</a> <a href="#',i,'" id=',i,'>',self.sentences[i],'. </a>'
			f.write('<a name="')
			f.write(str(i))
			f.write('">[')
			f.write(str(i))
			f.write(']</a> <a href="#')
			f.write(str(i))
			f.write('" id=')
			f.write(str(i))
			f.write('>')
			f.write(self.sentences[k])
			f.write('. </a>\n')
			i = i + 1

		f.write("</body>\n")
		f.write("</html>\n")

	def print_sent_ordered(self):
		s = sorted(self.clust_sentences,key=int)
		print s
		for i in s:
			print self.sentences[i]
			


