# 抓取ptt stream版的網頁原始碼( HTML )
import urllib.request as req 
import bs4
import re
import csv

HEADERS = {
    "Cookie": "over18=1"
}

def getArticleTime(article_url):
    try:
        request = req.Request(article_url, headers={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
        })
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")
        root = bs4.BeautifulSoup(data, "html.parser")

        meta_values = root.select("span.article-meta-value")
        if len(meta_values) >= 4:
            return meta_values[3].get_text(strip=True)

        # ✅ 備援：抓全文內是否有完整格式
        m = root.find(
            "span",
            class_="article-meta-value",
            string=re.compile(r"^\w{3} \w{3} \d{1,2} \d{2}:\d{2}:\d{2} \d{4}$")
        )
        return m.get_text(strip=True) if m else ""

    except Exception:
        return ""

    #     time_tag = root.find("span", class_="article-meta-value", string=re.compile(r"\w{3} \w{3} \d{1,2} \d{2}:\d{2}:\d{2} \d{4}"))
    #     if time_tag:
    #         return time_tag.text.strip()
    #     else:
    #         return ""
    # except Exception:
    #     return ""

def getData(url):

    # 建立request物件, 附加 request Headers 的資訊
    request=req.Request(url, headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
    })
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")

    # 解析原始碼，取得資料
    root=bs4.BeautifulSoup(data, "html.parser")
    items=root.find_all("div", class_="r-ent") # 尋找 class="title" 的div標籤

    page_articles = []
    for item in items:
        title_div = item.find("div", class_="title")
        title_tag = title_div.a if title_div else None

        if title_tag is not None:
            title = title_tag.string.strip()
            article_url = "https://www.ptt.cc" + title_tag["href"]
        else:
            title = "" # 被刪除文章以空白字串處理
            article_url = ""
        
        # 推文數、按讚數
        nrec_tag = item.find("div", class_="nrec")
        like_count = nrec_tag.text.strip() if nrec_tag else ""
        # 若顯示 "爆"=100 或 "x" =
        if like_count == "爆":
            like_count = "100"
        elif like_count.startswith("x") or like_count.startswith("x"):
            like_count = "-" + like_count[1:]
        elif like_count == "":
            like_count = "0"

        # 解析內文取得時間
        publish_time = getArticleTime(article_url) if article_url else ""

        page_articles.append([title, like_count, publish_time])
        print(f"{title},{like_count},{publish_time}")
        
    # 抓取下一頁連結       
    nextLink=root.find("a", string="‹ 上頁") # 找到內文是上頁的標籤
    next_href = nextLink["href"] if nextLink else None # 上一頁
    return next_href, page_articles

# 抓取一個頁面的標題
pageURL="https://www.ptt.cc/bbs/Steam/index.html"
count=0
all_articles = []

while count<3 and pageURL: #抓前三頁
    nextPage, page_articles = getData(pageURL)
    all_articles.extend(page_articles)
    if not nextPage:
        break
    pageURL="https://www.ptt.cc"+ nextPage
    count+=1 


# 輸出為 csv檔
with open("articles.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerows(all_articles)

print("已完成")  
