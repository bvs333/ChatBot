# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 17:14:35 2019

@author: bvsre
"""

import nltk
import random
import string 


predefined_responses = open('manipal_resp.txt','r')
responses = predefined_responses.read()
responses = responses.lower()

sentences = nltk.sent_tokenize(responses) 


lemmeatizer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmeatizer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


greeting_ip = ("hello", "hi", "greetings", "sup", "what's up","hey",)
greeting_op = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

def greeting_answer(sentence):
    for word in sentence.split():
        if word.lower() in greeting_ip:
            return random.choice(greeting_op)


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def answer(user_input):
    response = ''
    sentences.append(user_input)
    tfidf = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    chatbot = tfidf.fit_transform(sentences)
    vals = cosine_similarity(chatbot[-1], chatbot)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        response = 'Sorry I did not understand you '
        return response
    else:
        response = sentences[idx]
        return response


print("Jarvis: My name is Jarvis. I will answer your queries about Manipal University Jaipur. If you want to exit, type Bye!")

while(True):
    user_response = raw_input()
    user_response=user_response.lower()
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you' ):
            print("Jarvis: You are welcome..")
            break
        else:
            if(greeting_answer(user_response)!=None):
                print("Jarvis: "+greeting_answer(user_response))
            else:
                print("Jarvis: "+answer(user_response))
                sentences.remove(user_response)
    else:
        print("Jarvis: Bye! take care..")   
        break