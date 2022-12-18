import json
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
test = open('JSONcrawler.json',encoding="utf8") #開檔
Data = json.load(test) #反序列化(decode)
temp = Data.get('Article') #取得 key = "Title" 的 value

'''
li_avg = []
for i in temp:
    #print(i['瀏覽次數'])
    li_avg.append(int(i['瀏覽次數']))
series = pd.Series(li_avg)
print(series.describe())
mean = 867.548000
'''

avg = 0
count = 0
for i in temp:
    #print(i['瀏覽次數'])
    avg += int(i['瀏覽次數'])
    count += 1

li_analysis = []
for i in temp:
    if int(i['瀏覽次數']) > avg/count:
        li_analysis.append(i['標籤'])

#print(li_analysis)

dic_analysis = {}
for i in li_analysis:
    for j in i:
        dic_analysis[j] = dic_analysis.get(j,0)+1

li_quartile = []
for i in dic_analysis:
    li_quartile.append(dic_analysis[i])

series = pd.Series(li_quartile)
series_describe = series.describe()
print(series_describe)
mean = series_describe['mean']

count = 0
li_key = []
li_value = []
for i in dic_analysis:
    if dic_analysis[i] > mean:
        li_key.append(i)
        li_value.append(dic_analysis[i])
        print(i,':',dic_analysis[i])

#把dic中的key和value抽取出來，以便下方製作圖使用
li_key = []
li_value = []
for i in dic_analysis:
    if count>100:
        break
    if dic_analysis[i]>mean:
        li_key.append(i)
        li_value.append(dic_analysis[i])
        count += 1




#把網路上下載的字體加入
myfont = FontProperties(fname=r'./NotoSerifTC-Black.otf')

#設定圖片輸出的資訊
plt.figure(figsize=(20,20))
plt.title("Correlation of Views and Tags")
plt.xlabel("Tag")
x = range(len(li_key))
plt.xticks(rotation=30,ha = "right")
plt.ylabel("Frequency")
plt.bar(li_key,li_value)
plt.xticks(x,li_key,fontproperties=myfont)
plt.savefig("Correlation of Views and Tags Chart")
plt.show()
