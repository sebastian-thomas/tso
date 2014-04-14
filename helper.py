
import math
import sys

def uniqueterms(sentences):
	unique_terms = []
	for sentence in sentences:
		terms = sentence.split()
		for term in terms:
			if term not in unique_terms:
				unique_terms.append(term)
	return unique_terms


def word_count_list(word,list):
	count = 0;
	for w in list:
		if w == word:
			count = count + 1
	return count

def word_vector(sentences,uk_terms = "none"):
	unique_terms = uniqueterms(sentences)
	sentences_weight = []
	for sent in sentences:
		v = {}
		for word in unique_terms:
			v[word] = word_count_list(word,sent.split())
		sentences_weight.append(v)
	return sentences_weight


def tfisf(sentences,uk_terms = "none"):
	unique_terms = []
	unique_term_count = {}
	no_of_sentences = len(sentences);
	sentence_word_count = {}
	sentences_term_count = []
	sentences_weight = []
	sentences_tf = []
	tf = []
	isf = {}

	if(uk_terms == "none"):
		unique_terms = uniqueterms(sentences)
	else:
		unique_terms = uk_terms

	for term in unique_terms:
		unique_term_count[term] = 0

	for term in unique_terms:
		sentence_word_count[term] = 0

	for sentence in sentences:
		t_term_count = {}
		for term in unique_terms:
			if term in sentence.split():
				#t_term_count[term] = 1
				t_term_count[term] = word_count_list(term,sentence.split())
				unique_term_count[term] +=1
				sentence_word_count[term] +=1
			else:
				t_term_count[term] = 0
		sentences_term_count.append(t_term_count)
	#print sentences_term_count

	no_of_words = 0
	for term in unique_term_count:
		no_of_words = no_of_words + unique_term_count[term]

	#finding tf-isf

	for term in unique_terms:
		isf [term] = math.log(no_of_sentences*1.0/(sentence_word_count[term]+1))

	

	for sentence in sentences:
		t_tf = {}
		#print sentence.split()
		for term in unique_terms:
			if term in sentence.split():
				#print 'inside...'
				m = len(sentence.split())
				#print m
				#t_tf[term] = (1.0/m*1.0)
				t_tf[term] = (1.0* sentence_word_count[term])/(no_of_words*1.0)
			else:
				t_tf[term] = 0
		sentences_tf.append(t_tf)
		#print t_tf

	#print 'finished t_tf'


	for sentence_row in sentences_tf:
		t_weight = {}
		for term in unique_terms:
			t_weight[term] = sentence_row[term] * isf[term]
		sentences_weight.append(t_weight)


	return sentences_weight


def find_similarity(p,q):
	pq = 0.0
	modp = 0.0
	modq = 0.0
	for col in p:
		pq = pq + p[col]*q[col]

	for col in p:
		modp = modp + p[col] * p[col]
	modp = math.sqrt(modp)
	#print modp,p

	for col in q:
		modq = modq + q[col] * q[col]
	modq = math.sqrt(modq)
	#print modq,q
	if modp == 0:
		return 0
	elif modq ==0:
		return 0
	else:
		return pq /(modp * modq)



def similarity(sentences1_weight,sentences2_weight):
	#to find the similarity between two sentence vectors
	mat = []
	for rowone in sentences1_weight:
		row = {}
		i = 0
		for rowtwo in sentences2_weight:
			row[i] = find_similarity(rowone, rowtwo)
			i = i + 1
		mat.append(row)
	return mat


