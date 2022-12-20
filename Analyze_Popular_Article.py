import json
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
test = open('JSONcrawler.json',encoding="utf8") #開檔
Data = json.load(test) #反序列化(decode)
temp = Data.get('Article') #取得 key = "Title" 的 value


# 這個是瀏覽次數的平均，高於這個平均我們定義他為熱門文章
li_avg = []
for i in temp:
    #print(i['瀏覽次數'])
    li_avg.append(int(i['瀏覽次數']))
series1 = pd.Series(li_avg)
series1_describe = series1.describe()
print("瀏覽次數:")
print(series1_describe)
avg = series1_describe['mean']


# 抓出高於"瀏覽次數"平均的"標籤"
li_analysis = []
for i in temp:
    if int(i['瀏覽次數']) > avg:
        li_analysis.append(i['標籤'])

#print(li_analysis)

# 統計抓出來的各"標籤"數目
dic_analysis = {}
for i in li_analysis:
    for j in i:
        dic_analysis[j] = dic_analysis.get(j,0)+1


# 把統計後的數目放進list，去找尋平均數
li_value_avg = []
for i in dic_analysis:
    li_value_avg.append(dic_analysis[i])
series2 = pd.Series(li_value_avg)
series2_describe = series2.describe()
print("\n標籤:")
print(series2_describe)
print("\n")
max = series2_describe['max']


# 利用平均數製作圖表後，發現如果只是利用平均數去篩選，圖表內容會太過龐大，於是觀察圖標，找出"標籤"數量大於10是一個不錯的製圖選擇
count = 0
li_key = []
li_value = []
for i in dic_analysis:
    if dic_analysis[i] > max/10:
        li_key.append(i)
        li_value.append(dic_analysis[i])
        print(i,':',dic_analysis[i])



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
plt.savefig("Correlation of Views and Tags Chart (Fault)")
plt.show()
