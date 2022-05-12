#https://github.com/gutfeeling/word_forms
""" Installation:

git clone https://github.com/gutfeeling/word_forms.git
sudo pip install -e word_forms

"""

from word_forms.word_forms import get_word_forms
from nltk.corpus import wordnet as wn
from itertools import chain
from app.models import Tag
from app.models import Tag, TextualResponse
from nltk import word_tokenize
from nltk.corpus import stopwords
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import defaultdict

analyzer = SentimentIntensityAnalyzer()


tags = list()
# tags = list(Tag.objects.all())
tags_synonyms = {tag:set(chain.from_iterable([word.lemma_names() for word in wn.synsets(tag.tag_title)])) for tag in tags}
optimised_tags = {}
stop = set(stopwords.words('english'))

for tag,syns in tags_synonyms.items():
	optimised_tags[tag] = set()
	for syn in syns:
		words = get_word_forms(syn)
		
		for key,values in words.items():
			for word in values:
				optimised_tags[tag].add(word)

def get_sentiments(response):
	sentiment_dict = {
		'pos': 0,
		'neg': 0,
		'neu': 0
	}
	for line in response:
		for sentence in response.split("."):
			ret = get_sentiment(sentence)
			sentiment_dict[ret] += 1
	if sentiment_dict['pos'] + sentiment_dict['neg'] == 0:
		return 50.0
	return round(100 * (sentiment_dict['pos'] / (sentiment_dict['pos'] + sentiment_dict['neg'])), 1) 

def get_sentiment(sentence):
	vs = analyzer.polarity_scores(sentence)
	vs.pop('compound')
	type = max(vs.items(),key=lambda x:x[1])[0]
	print("Sentiment is",type)
	return type

def get_tags(sentence):
	optimised_sentence =  [i for i in sentence.lower().split() if i not in stop]
	print(optimised_sentence)

	#compare two lists 
	tags_in_sentence = []
	for word in optimised_sentence:
		for key,values in optimised_tags.items():
			if word in values:
					tags_in_sentence.append(key.tag_id)
	print("Tags in the sentence are",tags_in_sentence)
	if len(tags_in_sentence) == 0:
		return -1
	else:
		return tags_in_sentence[0]