import urllib.request as req #引入urllib模組中函式名稱為request的函式為req
import bs4 #引入bs4模組
import re #引入re模組
#定義函式getData，用以取得每一頁所有標題、標籤及內文。參數為網址
def getData(url,count,pages):
    #建立一個Request物件，附加Request Headers的資訊
    request = req.Request(url,headers = {
        "User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36"
    })
    
    #打開request
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")

    root = bs4.BeautifulSoup(data,"html.parser") #讓BeautifulSoup解析HTML格式文件
    all_titles = root.find_all("h3",class_="qa-list__title") #以列表形式找出所有class_=title的h3標籤


    #開啟JSONcrawler.json並用a模式保留原本資料並將新的資料寫入
    with open("JSONcrawler.json",mode = "a",encoding = "utf-8") as ftext:
        #此迴圈會找出該頁所有標題、標籤、詢問時間、瀏覽次數及內文
        for title in all_titles:
            title.a.string = re.sub(r"\"","'",title.a.string) #利用regex將 " 改成 ' ，以免語法錯誤
            title.a.string = re.sub(r"\\"," BACKSLASH ",title.a.string) #利用regex將 \ 改成 BACKLASH ，以免語法錯誤
            ftext.write("\n   {\n") #寫入與JSON檔的檔案格式有關的detail
            ftext.write("   \"標題\":"+"\""+title.a.string+"\","+"\n") #將內文的標題寫入JSON檔裡
            print("標題 : "+title.a.string)
            
            ftext.write("   \"標籤\":[") #寫入與JSON檔的檔案格式有關的detail

            url2 = title.a["href"] #將內文的網址存到url2裡

            #建立一個Request物件，附加Request Headers的資訊
            request2 = req.Request(url2,headers = {
                "User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36"
            })

            #打開request2
            with req.urlopen(request2) as response2:
                data2 = response2.read().decode("utf-8")
            
            root2 = bs4.BeautifulSoup(data2,"html.parser") #讓BeautifulSoup解析HTML格式文件
            contents = root2.find("div",class_="markdown__style").text #找出內文
            tags = root2.find("div",class_="qa-header__tagGroup") #以列表形式找出所有 class_=qa-header__tagGroup 的 div 標籤
            time_and_view = root2.find("div",class_="qa-header__info").text.split() #以列表形式找出所有 class_=qa-header__info 的 div 標籤
            
            #利用regex將會影響JSON的符號做替換
            contents = re.sub(r"\"","'",contents)
            contents = re.sub(r"\\"," BACKSLASH ",contents)
            contents = re.sub(r"\n","EOL",contents)
            contents = re.sub(r"\t","    ",contents)

            set_of_tags = set(tags.text.split("\n")) #利用集合將重複出現的標籤強制讓它出現一次
            #將集合內的資料重新裝回list內
            list_of_tags = []
            for i in set_of_tags:
                i = re.sub(r"\\"," BACKSLASH ",i)
                i = re.sub(r"\"","'",i)
                list_of_tags.append(i)
            
            #將標籤寫進JSON檔
            for tag in list_of_tags[1:]:
                if (tag!=list_of_tags[-1]):
                    ftext.write("\"" + tag + "\",")
                else:
                    ftext.write("\"" + tag + "\"],\n")
            
            print("標籤 :",end = " ")
            for tag in list_of_tags[1:]:
                print(tag,end = " ")
            
            ftext.write("   \"詢問時間\":\""+time_and_view[1]+"\",\n") #將詢問時間寫入JSON檔
            print("\n詢問時間 : "+time_and_view[1])
            ftext.write("   \"瀏覽次數\":\""+time_and_view[-2]+"\",\n") #將瀏覽次數寫入JSON檔
            print("瀏覽次數 : "+time_and_view[-2])

            #將內文寫入JSON檔
            if ( (count==pages-1) and (title.a.string == all_titles[-1].a.string)):
                ftext.write("   \"內文\":\""+contents+"\"\n") #將內文寫入content.txt裡
                ftext.write("   }]\n}")
                print("內文 : "+contents)
            else:
                ftext.write("   \"內文\":\""+contents+"\"\n")
                ftext.write("   },\n")
                print("內文 : "+contents+"\n\n")


    #抓取下一頁的連結
    nextLink = root.find("a",string="下一頁") #找到內文是 下一頁 的標籤a
    return nextLink["href"] #回傳下一頁的網址

#寫入與JSON檔的檔案格式有關的detail
with open("JSONcrawler.json",mode = "a",encoding = "utf-8") as ftext:
    ftext.write("{\n")
    ftext.write("   \"Article\":[")
pageURL = "https://ithelp.ithome.com.tw/" #將起始網頁的網址存到pageURL裡
count = 0 #count用來表示想抓取幾頁
pages = int(input("Please enter how many pages you want to crawl:"))
#重複抓取每頁資料
while count<pages:
    pageURL = getData(pageURL,count,pages) #將 return 回來的網址覆蓋到pageURL上，以便重複利用
    count += 1 #執行完一次後增加1，以確保能抓到預期的頁數
