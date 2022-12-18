import json
import pandas as pd
import re
import jieba
import jieba.analyse
test = open('JSONcrawler.json',encoding="utf8") #開檔
Data = json.load(test) #反序列化(decode)
temp = Data.get('Article') #取得 key = "Article" 的 value


#計算不同"標籤"出現次數
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
    print(li_key_sorted[i],":",li_value[i])


# 做出文字雲
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