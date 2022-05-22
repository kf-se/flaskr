from flask import (
    current_app, g
)
import pandas as pd
import numpy as np
import re
import nltk
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer



def sentiment(body):
    mapper = {0:'Unhappy', 1:'Happy'}
    # load CountVectorizer, nlp model, porterstemmer
    #resource_path = os.path.join(current_app.root_path, 'resources/')
    #nlp_model = pickle.load(open(resource_path + 'gnb_nlp_model.pickle', 'rb'))
    #cv = pickle.load(open(resource_path + 'cv_nlp.pickle', 'rb'))
    ps = PorterStemmer()
    # preprocess text body with re.sub and PorterStemmer, stopwords
    data = re.sub('[^a-zA-Z]', ' ', body)
    data = data.lower()
    data = data.split()
    all_stopwords = stopwords.words('english')
    all_stopwords.remove('not')
    data = [ps.stem(word) for word in data if not word in set(all_stopwords)]
    data = ' '.join(data)
    X = [data]
    # make sentiment
    X = g.cv.transform(X).toarray()
    y_pred = g.nlp_model.predict(X)

    return mapper[y_pred[0]]