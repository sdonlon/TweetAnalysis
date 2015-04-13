import sys
import re
import json
import numpy
from pprint import pprint

class sentscore(object):
    _lookup = None

    def __init__(self,sent_file):
        if sentscore._lookup is None:
            sentscore._lookup = self._build_lookup(sent_file)

    def _build_lookup(self,sent_file):
        scores = {} # initialize an empty dictionary
    
        for line in sent_file:
          term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
          scores[term] = int(score)  # Convert the score to an integer.

        #print scores.items() # Print every (term, score) pair in the dictionary
        return scores

    def get_score(self,word):
        return self._lookup.get(word,0)

def tweet_lines(fp):
    tweets = [] # initialize an empty list dictionary

    line = fp.readline()
    while len(line) is not 0:
      data = json.loads(line.strip())
      tweets.append(data)
      line = fp.readline()

    #pprint(tweets)
    return tweets

def parse_tweets(tweets):

    pattern = re.compile(r'\w+')
    parsed = []
    for t in tweets:
            if 'text' not in t.keys():
                    continue
 
            words = pattern.findall(t['text'])
            parsed.append(words)

    #pprint(parsed)       
    return parsed

def print_sentiments(sent_file,tweet_file):

    scores = sentscore(sent_file)
    tweets = tweet_lines(tweet_file)
    parsed = parse_tweets(tweets)

    tweetscore = []
    sums = []
    for word_list in parsed:
        tweet_scores = [scores.get_score(w) for w in word_list]
    
        tweetscore = zip(word_list, tweet_scores)
        pprint(tweetscore)
        summed = sum(tweet_scores)
        sums.append(summed)

    print "tweet_count: %s" % len(tweets)
    print "sum: %s" % str(sum(sums))
    print "mean: %f" % numpy.mean(sums)

   
def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    
    print_sentiments(sent_file, tweet_file)

    sent_file.close()
    tweet_file.close()

if __name__ == '__main__':
    main()