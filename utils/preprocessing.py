import numpy as np
from nltk.tokenize import sent_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def map_target(df, col_name='target'):
	return df[col_name].map({'propaganda':1,'non-propaganda':0})
	
def tokenize_text(text, word_to_idx):
    text = text.lower()
    tokens = word_tokenize(text)
    #tokens = np.vectorize(lambda x: word_to_idx.get(x, word_to_idx['UNK']))(tokens) #returns np array
    tokens = list(map(lambda x: word_to_idx.get(x, word_to_idx['UNK']), tokens)) #returns list
    return tokens

def process_df(df, text_processor, processor_args, get_len=True):	
    df['target'] = map_target(df)
    df['text']=df['text'].apply(lambda x: text_processor(x, **processor_args))
    if get_len:
        df['len']= df['text'].apply(lambda x: len(x))
    return df
	
def get_sentiment_features(df, text_col='text', id_col='id'):
    analyzer = SentimentIntensityAnalyzer()
    features = {'neg_max':[], 'neg_min':[], 'neg_median':[], \
                'pos_max':[], 'pos_min':[], 'pos_median':[], \
                'neu_max':[], 'neu_min':[], 'neu_median':[]}
    feature_fns = {'max':np.max, 'min':np.min, 'median':np.median}
    
    for text in df[text_col]:
        vs_lists = {'neg':[], 'pos':[], 'neu':[]}
        for sent in sent_tokenize(text):
            vs = analyzer.polarity_scores(sent)
            for k in vs_lists.keys():
                vs_lists[k].append(vs[k])

        for k, vs_list in vs_lists.items():
            for f, fn in feature_fns.items():
                features[k+'_'+f].append(fn(vs_list))
                
    features['id'] = df[id_col].values.tolist()            
    return features