def max_similarity(docu,ordered,clust_sentences):
	maxsim = 0
	for j in range(len(clust_sentences)):
		if clust_sentences[j] not in ordered:
			if maxsim == 0:
				maxsim = j
			else:
				if docu.sent_similarity[ordered[len(ordered)-1]][j]>docu.sent_similarity[ordered[len(ordered)-1]][maxsim]:
					maxsim=j
	return maxsim



def similarity_ordering(doc,clust_sentences):
	ordered_sent = []
	ordered_sent.append(clust_sentences[0])
	#print ordered_sent
	#print "  "
	for i in range(1,len(clust_sentences)):
		maxval=max_similarity(doc,ordered_sent,clust_sentences)
		ordered_sent.append(clust_sentences[maxval])
	return ordered_sent

def find_precedence(doc,sent,clust_sentences):
	precedence = []
	maxprev = sent
	maxsuc = sent
	#print sent
	for j in range(len(clust_sentences)):
		if clust_sentences[j] == sent:
			precedence.append(0.5)
		else:
			if sent-1!=0:
				if doc.sent_similarity[sent][clust_sentences[j]]<doc.sent_similarity[sent-1][clust_sentences[j]]:
					maxprev = sent-1
				if sent-2!=0:
					if doc.sent_similarity[maxprev][clust_sentences[j]]<doc.sent_similarity[sent-2][clust_sentences[j]]:
						maxprev = sent-2
					if sent-3!=0:
						if doc.sent_similarity[maxprev][clust_sentences[j]]<doc.sent_similarity[sent-3][clust_sentences[j]]:
							maxprev = sent-3
						if sent-4!=0:
							if doc.sent_similarity[maxprev][clust_sentences[j]]<doc.sent_similarity[sent-4][clust_sentences[j]]:
								maxprev = sent-4
			prev_sim = doc.sent_similarity[maxprev][clust_sentences[j]]
			if sent+1!=0:
				if doc.sent_similarity[sent][clust_sentences[j]]<doc.sent_similarity[sent+1][clust_sentences[j]]:
					maxsuc = sent+1
				if sent+2!=0:
					if doc.sent_similarity[maxsuc][clust_sentences[j]]<doc.sent_similarity[sent+2][clust_sentences[j]]:
						maxsuc = sent+2
					if sent+3!=0:
						if doc.sent_similarity[maxsuc][clust_sentences[j]]<doc.sent_similarity[sent+3][clust_sentences[j]]:
							maxsuc = sent+3
						if sent+4!=0:
							if doc.sent_similarity[maxsuc][clust_sentences[j]]<doc.sent_similarity[sent+4][clust_sentences[j]]:
								maxsuc = sent+4
			succ_sim = doc.sent_similarity[maxsuc][clust_sentences[j]]
			if(prev_sim>succ_sim):
				precedence.append(0.0)
			elif prev_sim<succ_sim:
				precedence.append(1.0)
			else:
				precedence.append(0.5)

	return precedence


def precedence_ordering(doc,clust_sentences):
	ordered_sentences = []
	precedence_matrix = []
	#ordered_sentences.append(clust_sentences[0])
	for i in range(len(clust_sentences)):
		precedence_matrix.append(find_precedence(doc,clust_sentences[i],clust_sentences))
	#print precedence_matrix
	maxp = {}
	for i in range(len(precedence_matrix)):
		maxp[i] = 0
		for j in range(len(precedence_matrix[i])):
			#print i,j
			if precedence_matrix[i][j] == 0.0:
				maxp[i] = maxp[i]+1
	
	maxprec = 0
	for j in range(1,len(maxp)):
		if maxp[j]>maxp[maxprec]:
			maxprec = j
	#maxprec contains position of the sentence that is to be placed first.  
	return maxprec
