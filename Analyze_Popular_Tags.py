import json
import pandas as pd
import re
import jieba
import jieba.analyse
test = open('JSONcrawler.json',encoding="utf8") #開檔
Data = json.load(test) #反序列化(decode)
temp = Data.get('Article') #取得 key = "Title" 的 value


df = pd.DataFrame(temp)
df['seg'] = ""


jieba.analyse.set_stop_words('stopwords.txt')
index = 0
li_jieba = []

for documents in df['內文']:
    documents = re.sub(r"[a-zA-Z0-9]","",documents)
    documents = re.sub(r"_","",documents)
    documents = re.sub(r"一.","",documents)
    documents = re.sub(r"三.","",documents)
    documents = re.sub(r"三..","",documents)
    documents = re.sub(r"但.","",documents)
    documents = re.sub(r"還.","",documents)
    seg_list = jieba.analyse.extract_tags(documents, 150)
    li_jieba.append(seg_list)
    #seg_list = jieba.lcut(documents)
    df['seg'].iloc[index] = seg_list
    df['內文'].iloc[index] =  documents
    index += 1



#印出不同"標籤"出現次數
dic = {} #紀錄下面取得的不同"標籤"出現次數
for i in temp: #從 list 中一個一個列舉出 dict
    #print(li['標籤'])
    for j in i['標籤']: #列舉出每個 key = "標籤" 的 value
        dic[j] = dic.get(j,0)+1 #檢查"標籤"中的每個字串是否出現在 dic 中。如果沒出現，則加入 dic 裡，並使其 value=1 ; 否則已經出現就將其 value+1


li_key = []
li_value = []
for i in dic:
    li_key.append(i) #將每個標籤名稱加入 list 中
    li_value.append(dic[i]) #將每個標籤出現過的次數加入 list 中
#排序 (由高到低排序"標籤出現的次數")
li_value.sort(reverse = True) #將"標籤出現次數"由大到小排序
li_key_sorted = [] #存放排序好的"標籤"
length = len(li_key) #"標籤"總數

#利用迴圈排序"標籤"
for i in range(length):
    for j in dic:
        if li_value[i] == dic[j]:
            li_key_sorted.append(j)

dic_sort = {}
#利用迴圈印出排序後的結果
for i in range(length):
    dic_sort[li_key_sorted[i]] = li_value[i]
    #print(li_key_sorted[i],":",li_value[i])

from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud

import numpy as np
mask = np.array(Image.open("IT.png"))
font = "C:\Windows\Fonts\MSJH.TTC"

wordcloud = WordCloud(background_color = "white", font_path=font, mask = mask)
wordcloud.generate_from_frequencies(dic)

plt.figure(figsize=(20,20))
plt.imshow(wordcloud)
plt.axis("off")
plt.savefig("Word Cloud")
plt.show()


Top5 = {}
count = 0
for i in dic_sort:
    if count>=1:
        break
    Top5[i] = dic_sort[i]
    count += 1
print(Top5)

res = pd.DataFrame(columns = ['tag','seg'],index = range(count))
cnt = 0
for tag in Top5:
    res['tag'][cnt] = tag
    cnt += 1


count = 0
for tag in Top5:
    id = 0
    li_id = []
    for seg in df['標籤']:
        if tag in seg:
            li_id.append(id)
        id += 1
    big_list = []
    for i in li_id:
        for seg in df['seg'][i]:
            big_list.append(seg)
    res['seg'][count] = big_list
    count += 1
print(res)

res.to_csv("After_analysis.csv")