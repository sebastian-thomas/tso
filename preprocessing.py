from nltk.corpus import stopwords
from nltk import stem

def load_sentences(input_files):
	paragraphs = []
	sentences = []
	t_sentences = []
	t_words = []
	for input_file in input_files:
		f = open(input_file, "r")
		for line in f :
			paragraphs.append(line.lower())
	
	#sentence segments
	for paragraph in paragraphs:
		t2_sentences = sentence_segmentation(paragraph)
		for t in t2_sentences:
			t_sentences.append(t)

	for sentence in t_sentences:
		if len(sentence) > 3:
			sentences.append(sentence)

	return sentences


def sentence_segmentation(paragraph):
	#to take sentence by sentance from paragraphs
	return paragraph.split('.')

def remove_stopwords(sentences):
	#remove stop words
	t_sentences = []
	for sentence in sentences:
		t_stop = ' '.join([stem_word(word) for word in sentence.split() if word not in(stopwords.words('english'))])
		t_sentences.append(t_stop)
	return t_sentences

def stem_word(word):
	#stemming of words
	new_word=word.replace(",","")
	new_word=new_word.replace("\'","")
	stemmer = stem.PorterStemmer()
	return stemmer.stem(new_word)