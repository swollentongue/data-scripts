import sys
from collections import defaultdict
import re
import praw

'''
Counts ngrams of a given subreddit. Outputs seen subtring, it's ngram type, and the frequency

'''

target_sub = sys.argv[1]
r = praw.Reddit('post scraper by /u/ADDUSERNAMEHERE')
subreddit = r.get_subreddit(target_sub)
output_filename = target_sub + '_reddit_ngrams.txt'

ngram_counts = defaultdict(int)
stop_words = set('all', 'show', 'anyway', 'four', 'latter', 'go', 'mill', 'find', 'seemed', 'one', 'whose', 'everything', 'herself', 'whoever', 'enough', 'should', 'to', 'only', 'under', 'do', 'his', 'get', 'very', 'de', 'none', 'cannot', 'every', 'during', 'him', 'becomes', 'did', 'cry', 'these', 'she', 'thereupon', 'where', 'ten', 'eleven', 'namely', 'are', 'further', 'sincere', 'even', 'what', 'please', 'yet', 'behind', 'above', 'between', 'neither', 'ever', 'across', 'thin', 'we', 'full', 'never', 'however', 'here', 'others', 'hers', 'along', 'fifteen', 'both', 'last', 'many', 'whereafter', 'wherever', 'against', 'etc', 's', 'became', 'whole', 'otherwise', 'among', 'via', 'co', 'afterwards', 'seems', 'whatever', 'alone', 'moreover', 'throughout', 'from', 'would', 'two', 'been', 'next', 'few', 'much', 'call', 'therefore', 'interest', 'themselves', 'thru', 'until', 'empty', 'more', 'fire', 'beforehand', 'hereby', 'herein', 'everywhere', 'former', 'those', 'must', 'me', 'myself', 'this', 'bill', 'will', 'while', 'anywhere', 'nine', 'can', 'of', 'my', 'whenever', 'give', 'almost', 'is', 'thus', 'it', 'cant', 'itself', 'something', 'in', 'ie', 'if', 'perhaps', 'six', 'amount', 'same', 'wherein', 'beside', 'how', 'several', 'see', 'may', 'after', 'upon', 'hereupon', 'such', 'a', 'off', 'whereby', 'third', 'together', 'i', 'well', 'rather', 'without', 'so', 'the', 'con', 'yours', 'just', 'less', 'being', 'indeed', 'over', 'move', 'front', 'already', 'through', 'yourselves', 'fify', 'still', 'its', 'before', 'thence', 'somewhere', 'thick', 'had', 'except', 'ours', 'has', 'might', 'thereafter', 'then', 'them', 'someone', 'around', 'thereby', 'five', 'they', 'not', 'now', 'nor', 'name', 'hereafter', 'always', 'whither', 't', 'each', 'become', 'side', 'therein', 'twelve', 'because', 'often', 'doing', 'eg', 'some', 'back', 'our', 'beyond', 'ourselves', 'out', 'for', 'bottom', 'although', 'since', 'forty', 'per', 're', 'does', 'three', 'either', 'be', 'sixty', 'whereupon', 'nowhere', 'besides', 'found', 'put', 'anyhow', 'by', 'on', 'about', 'anything', 'theirs', 'could', 'keep', 'whence', 'due', 'ltd', 'hence', 'onto', 'or', 'first', 'own', 'seeming', 'formerly', 'into', 'within', 'yourself', 'down', 'everyone', 'done', 'another', 'couldnt', 'your', 'fill', 'her', 'whom', 'twenty', 'top', 'there', 'system', 'least', 'anyone', 'their', 'too', 'hundred', 'was', 'himself', 'elsewhere', 'mostly', 'that', 'becoming', 'nobody', 'but', 'somehow', 'part', 'with', 'than', 'he', 'made', 'whether', 'up', 'us', 'nevertheless', 'below', 'un', 'were', 'toward', 'and', 'describe', 'am', 'mine', 'an', 'meanwhile', 'as', 'sometime', 'at', 'have', 'seem', 'any', 'inc', 'again', 'hasnt', 'no', 'whereas', 'when', 'detail', 'also', 'other', 'take', 'which', 'latterly', 'you', 'towards', 'though', 'who', 'most', 'eight', 'amongst', 'nothing', 'else', 'why', 'don', 'noone', 'sometimes', 'amoungst', 'serious', 'having', 'once')
punctuation = re.compile(r'["\',.?!_\n\t-]|')
with open("stop_words.txt", "r") as cws: # stolen from https://github.com/rhiever/reddit-analysis
    for line in cws:
        stop_words.add(line.strip().lower())

def count_ngrams(text, ngram_range = (1,4)):
    '''Take a given piece of text, remove stop words, tokenize and populates dictionary with ngrams.'''
    
    # Normalize, tokenize, and remove stop words
    text = text.encode('utf-8', 'ignore')
    text = re.sub(punctuation, '', text)
    tokens = text.strip().lower().split()
    words = [t.strip() for t in tokens if t.strip() not in stop_words]
    
    # extract ngrams and populate ngram_counts
    if len(words) > 0:          
        for ngram_length in range(*ngram_range):
            ngrams = zip(*[words[i:] for i in range(ngram_length)])
            for token_ngram in ngrams:
                collapsed_ngram = ' '.join(token_ngram)
                ngram_counts[collapsed_ngram] += 1
    else:
        sys.stderr.write('Text Empty:\n' + text + '\n')

if __name__ == "__main__":
    for post in subreddit.get_hot(limit = 50):
        count_ngrams(post.selftext)
        count_ngrams(post.title)
    latest_comments = subreddit.get_comments(limit = 200)
    for comment in latest_comments:
        count_ngrams(comment.body)

    with open(output_filename, 'w') as w:
        for ngram in sorted(ngram_counts, key=ngram_counts.get, reverse = True):
            type = str(len(ngram.split())) + '-ngram'
            text = '{}\t{}\t{}\n'.format(ngram, type, str(ngram_counts[ngram]))
            w.write(text)



