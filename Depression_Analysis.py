#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import pandas as pd
import numpy as np


# In[2]:


fh=open('isear.txt')
label=[]
sen=[]
for line in fh:
    lis=re.findall('[a-zA-Z]+',line)
    label.append(lis[0])
    sen.append(' '.join(lis[1:]))


# In[3]:


print(label)


# In[4]:


print(sen)


# In[5]:


import csv


# In[6]:


with open ('data2.csv','w') as f:
    writer=csv.writer(f)
    writer.writerows(zip(label,sen))


# In[7]:


df=pd.read_csv('data2.csv')


# In[8]:


df.head()


# In[9]:


df.rename(columns={'ID':'label','CITY COUN SUBJ SEX AGE RELI PRAC FOCC MOCC FIEL EMOT WHEN LONG INTS ERGO TROPHO TEMPER EXPRES MOVE EXP EXP EXP PARAL CON EXPC PLEA PLAN FAIR CAUS COPING MORL SELF RELA VERBAL NEUTRO Field Field Field MYKEY SIT STATE':'sentence'},inplace=True)


# In[10]:


df.head()


# In[11]:


df.isnull().sum()


# In[12]:


import spacy
nlp=spacy.load('en')


# In[13]:


print(nlp.Defaults.stop_words)


# In[14]:


df.count()


# In[15]:


corpus=[]
for i in range(7666):
    sentence=re.sub('[^a-zA-Z]', ' ',df['sentence'][i])
    sentence=sentence.lower()
    sentence=sentence.split()
    
    sentence=[s for s in sentence if not nlp.vocab[s].is_stop]
    sentence=' '.join(sentence)
    corpus.append(sentence)


# In[16]:


corpus


# In[17]:


corpus2=[]
for i in range(7666):
    sent=nlp(corpus[i])
    
    sent2=[s.lemma_ for s in sent ]
    sentence2=' '.join(sent2)
    corpus2.append(sentence2)


# In[18]:


corpus2


# In[19]:


df.head()


# In[20]:


df['cleaned_sentence']=corpus2


# In[21]:


df.head()


# In[22]:


df.label.value_counts()


# In[23]:


get_ipython().system('pip install wordcloud')
from wordcloud import WordCloud
import matplotlib.cm
import matplotlib.pyplot as plt


# In[24]:


depressive_words = ' '.join(list(df[df['label'] == 'sadness']['cleaned_sentence']))
depressive_wc = WordCloud(width = 512,height = 512, collocations=False, colormap=matplotlib.cm.inferno).generate(depressive_words)
plt.figure(figsize = (8, 6), facecolor = 'k')
plt.imshow(depressive_wc)
plt.show()


# In[25]:


depressive_words = ' '.join(list(df[df['label'] == 'joy']['cleaned_sentence']))
depressive_wc = WordCloud(width = 512,height = 512, collocations=False, colormap=matplotlib.cm.inferno).generate(depressive_words)
plt.figure(figsize = (8, 6), facecolor = 'k')
plt.imshow(depressive_wc)
plt.show()


# In[26]:


df['emotion'] = df['label'].apply(lambda c: 'Positive' if c =='sadness' else 'Negative')


# In[27]:


df['emotion'].value_counts()


# In[28]:


df5=pd.read_csv('sentiment_tweets3.csv')


# In[29]:


df5.head()


# In[30]:


df5 = df5.drop(['Unnamed: 0'],axis=1)


# In[31]:


df5


# In[32]:


df5.label.value_counts()


# In[33]:


df5=df5.iloc[6000:]


# In[34]:


df5


# In[35]:


df5.info()


# In[36]:


corpus=[]
for i in range(6000,10314):
    sentence=re.sub('[^a-zA-Z]', ' ',df5['message'][i])
    sentence=sentence.lower()
    sentence=sentence.split()
    
    sentence=[s for s in sentence if not nlp.vocab[s].is_stop]
    sentence=' '.join(sentence)
    corpus.append(sentence)


# In[37]:


corpus2=[]
for i in corpus:
    sent=nlp(i)   
    sent2=[s.lemma_ for s in sent ]
    sentence2=' '.join(sent2)
    corpus2.append(sentence2)


# In[38]:


len(corpus2)


# In[39]:


corpus2


# In[40]:


df5['cleaned_sentence']=corpus2


# In[42]:


df5=df5[['label','message','cleaned_sentence']]

df5


# In[43]:


df


# In[44]:


df5


# In[45]:


df3=df5[df5['label']>=0]


# In[46]:


df4=df.append(df3)


# In[47]:


df4.head()


# In[48]:


df4['emotion'] = df4['label'].apply(lambda c: 'Positive' if c !=0 and c!='joy' else 'Negative')


# In[49]:


df4


# In[50]:


df4['emotion'].value_counts()


# In[51]:


df4.to_csv('cleaned_data.csv')


# In[52]:


from sklearn.model_selection import train_test_split



X = df4['cleaned_sentence']
y = df4['emotion']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=42)


# In[53]:


from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

text_clf = Pipeline([('tfidf', TfidfVectorizer()),
                     ('clf', LinearSVC()),
])

text_clf.fit(X_train, y_train) 


# In[54]:


def process(str):
    corpus=[]
    
    sentence=re.sub('[^a-zA-Z]', ' ',str)
    sentence=sentence.lower()
    sentence=sentence.split()
    
    sentence=[s for s in sentence if not nlp.vocab[s].is_stop]
    sentence=' '.join(sentence)
    
    
    
    sent=nlp(sentence)   
    sent2=[s.lemma_ for s in sent ]
    sentence2=' '.join(sent2)
    return(sentence2)


# In[55]:


string=str(input("Enter Message :"))
string2=process(string)   
z=pd.Series(string2)
predictions = text_clf.predict(z)
predictions


# In[56]:


predictions2=text_clf.predict(X_test)
from sklearn import metrics
print(metrics.confusion_matrix(y_test,predictions2))


# In[57]:


print(metrics.classification_report(y_test,predictions2))


# In[58]:


print(metrics.accuracy_score(y_test,predictions2))


# In[ ]:




