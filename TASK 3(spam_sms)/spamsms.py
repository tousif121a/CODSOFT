# -*- coding: utf-8 -*-
"""SpamSms.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VGDsQyQJB_RlrT6c4R-odsuwjS7HUc3z
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import re

raw_data = pd.read_csv('/content/spam.csv', encoding='latin1')
select_columns = ['v1', 'v2']
filter_data = raw_data[select_columns]

print(filter_data)

data=filter_data.where((pd.notnull(filter_data)),'')

data.shape

data.loc[data['v1']=='spam','v1',]=0
data.loc[data['v1']=='ham','v1',]=1

spam_count = data['v1'].value_counts()[0]
ham_indices = data[data['v1'] == 1].index
random_indices = np.random.choice(ham_indices, spam_count, replace=False)
balanced_indices = np.concatenate([data[data['v1'] == 0].index, random_indices])
balanced_data = data.loc[balanced_indices]

x = balanced_data['v2']
y = balanced_data['v1']

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=3)
print(x.shape)
print(x_train.shape)
print(x_test.shape)

feature_extraction=TfidfVectorizer(min_df=1,stop_words='english',lowercase=True)
x_train_features=feature_extraction.fit_transform(x_train)
x_test_features=feature_extraction.transform(x_test)

y_train=y_train.astype('int')
y_test=y_test.astype('int')

model=svm.SVC()
model.fit(x_train_features,y_train)

predictions = model.predict(x_train_features)
accuracy = accuracy_score(y_train, predictions)


print("Accuracy on training data is: ",accuracy)

predictions_test = model.predict(x_test_features)
accuracy = accuracy_score(y_test, predictions_test)

cm = confusion_matrix(y_test, predictions_test)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Spam', 'Ham'], yticklabels=['Spam', 'Ham'])
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')
plt.show()

print("Classification Report on testing data:\n", classification_report(y_test, predictions_test))

plt.figure(figsize=(6, 4))
sns.countplot(x='v1', data=balanced_data)
plt.title('Class Distribution')
plt.xlabel('Class')
plt.ylabel('Count')
plt.show()

input=["FreeMsg Hey there darling it's been 3 week's now and no word back! I'd like some fun you up for it still? Tb ok! XxX std chgs to send, å£1.50 to rcv"]

input_data_features=feature_extraction.transform(input)

predictions=model.predict(input_data_features)

if predictions[0]==1:
  print('Not spam mail')
else:
  print('Spam mail')

