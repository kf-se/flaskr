import pandas as pd
import numpy as np
import os
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

def sentiment(body):
    # load CountVectorizer 
    # load nlp model
    # preprocess text body with re.sub and PorterStemmer, stopwords
    # make sentiment
    return body[0]