import sys
from collections import defaultdict
import re

'''
Counts character ngrams of a given corpus. Outputs seen subtring, it's ngram type, and the frequency

Usage:
    cat targetfile | python substr_counting.py > outputfilname

TODO:
* Add logic to dynamically choose range of ngrams at the command line
* Combine token ngram and character ngram counting scripts and allow user to decide which they need.
* Add logic that allows preserving multiple columns.
* Add the ability weigh individual ngrams according to positive/negative training data

'''

# target_file = sys.argv[1]
ngram_counts = defaultdict(int)

stopwords = ['all', 'show', 'anyway', 'four', 'latter', 'go', 'mill', 'find', 'seemed', 'one', 'whose', 'everything', 'herself', 'whoever', 'enough', 'should', 'to', 'only', 'under', 'do', 'his', 'get', 'very', 'de', 'none', 'cannot', 'every', 'during', 'him', 'becomes', 'did', 'cry', 'these', 'she', 'thereupon', 'where', 'ten', 'eleven', 'namely', 'are', 'further', 'sincere', 'even', 'what', 'please', 'yet', 'behind', 'above', 'between', 'neither', 'ever', 'across', 'thin', 'we', 'full', 'never', 'however', 'here', 'others', 'hers', 'along', 'fifteen', 'both', 'last', 'many', 'whereafter', 'wherever', 'against', 'etc', 's', 'became', 'whole', 'otherwise', 'among', 'via', 'co', 'afterwards', 'seems', 'whatever', 'alone', 'moreover', 'throughout', 'from', 'would', 'two', 'been', 'next', 'few', 'much', 'call', 'therefore', 'interest', 'themselves', 'thru', 'until', 'empty', 'more', 'fire', 'beforehand', 'hereby', 'herein', 'everywhere', 'former', 'those', 'must', 'me', 'myself', 'this', 'bill', 'will', 'while', 'anywhere', 'nine', 'can', 'of', 'my', 'whenever', 'give', 'almost', 'is', 'thus', 'it', 'cant', 'itself', 'something', 'in', 'ie', 'if', 'perhaps', 'six', 'amount', 'same', 'wherein', 'beside', 'how', 'several', 'see', 'may', 'after', 'upon', 'hereupon', 'such', 'a', 'off', 'whereby', 'third', 'together', 'i', 'well', 'rather', 'without', 'so', 'the', 'con', 'yours', 'just', 'less', 'being', 'indeed', 'over', 'move', 'front', 'already', 'through', 'yourselves', 'fify', 'still', 'its', 'before', 'thence', 'somewhere', 'thick', 'had', 'except', 'ours', 'has', 'might', 'thereafter', 'then', 'them', 'someone', 'around', 'thereby', 'five', 'they', 'not', 'now', 'nor', 'name', 'hereafter', 'always', 'whither', 't', 'each', 'become', 'side', 'therein', 'twelve', 'because', 'often', 'doing', 'eg', 'some', 'back', 'our', 'beyond', 'ourselves', 'out', 'for', 'bottom', 'although', 'since', 'forty', 'per', 're', 'does', 'three', 'either', 'be', 'sixty', 'whereupon', 'nowhere', 'besides', 'found', 'put', 'anyhow', 'by', 'on', 'about', 'anything', 'theirs', 'could', 'keep', 'whence', 'due', 'ltd', 'hence', 'onto', 'or', 'first', 'own', 'seeming', 'formerly', 'into', 'within', 'yourself', 'down', 'everyone', 'done', 'another', 'couldnt', 'your', 'fill', 'her', 'whom', 'twenty', 'top', 'there', 'system', 'least', 'anyone', 'their', 'too', 'hundred', 'was', 'himself', 'elsewhere', 'mostly', 'that', 'becoming', 'nobody', 'but', 'somehow', 'part', 'with', 'than', 'he', 'made', 'whether', 'up', 'us', 'nevertheless', 'below', 'un', 'were', 'toward', 'and', 'describe', 'am', 'mine', 'an', 'meanwhile', 'as', 'sometime', 'at', 'have', 'seem', 'any', 'inc', 'again', 'hasnt', 'no', 'whereas', 'when', 'detail', 'also', 'other', 'take', 'which', 'latterly', 'you', 'towards', 'though', 'who', 'most', 'eight', 'amongst', 'nothing', 'else', 'why', 'don', 'noone', 'sometimes', 'amoungst', 'serious', 'having', 'once']
punctuation = re.compile(r'["\',.?!_]')

def process_line(line, ngram_range = (3, 6)):
    '''Take a given line, splits it into tokens and count char ngrams of individual tokens.
    populates ngram_counts dict, returns nothing.'''
    
    # Normalize, tokenize, and remove stop words
    line = line.decode('utf-8')
    line = re.sub(punctuation, '', line)
    tokens = line.strip().lower().split()
    words = [t.strip() for t in tokens if t.strip() not in stopwords]
    
    # extract char ngrams and populate ngram_counts
    if len(tokens) > 0:          
        for ngram_length in range(*ngram_range):
            for token in words:
                tok_length = len(token)
                if tok_length >= ngram_length:
                    for i, char in enumerate(token):
                        if i == tok_length - ngram_length:
                            break
                        upper = i + ngram_length
                        char_ngram = token[i:upper]
                        ngram_counts[char_ngram] += 1
    else:
        sys.stderr.write('Line has too few tokens. Skipping.\n')

if __name__ == "__main__":
    for line in sys.stdin:
        process_line(line, ngram_range = (3, 6))

    sys.stdout.write('Substring\tType\tFrequency\n')
    for ngram in sorted(ngram_counts, key = ngram_counts.get, reverse = True):
        type = str(len(ngram)) + '-gram'
        outstr = '{}\t{}\t{}\n'.format(ngram, type, ngram_counts[ngram])
        sys.stdout.write(outstr.encode('utf-8'))