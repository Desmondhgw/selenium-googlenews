from selenium import webdriver
import time
import pandas as pd

PATH = "D:\chromedriver.exe"
driver = webdriver.Chrome(PATH)
articles =[]
url =''
main_query = ''
main_region = ''
status = True

def craft_url(query, region, start, end):
    global url, main_query, main_region, main_start, main_end
    main_query = query
    main_region = region

    url = f'https://www.google.com/search?q={query}&rlz=1C1ONGR_en{region}933SG933&tbs=cdr:1,cd_min:{start},cd_max:{end},sbd:1&tbm=nws&sxsrf=ALeKk01aflpQNP1ZZ_T4be6c1j0AaGca-g:1629088758656&source=lnt&sa=X&ved=2ahUKEwiVoJHG3LTyAhUIA3IKHUJTA3gQpwV6BAgHECw&biw=1920&bih=969&dpr=1'
    driver.get(url)
    print(url)


def append_articles():
    posts = driver.find_elements_by_css_selector("div[class='dbsr']")
    for post in posts:
        title = post.find_element_by_css_selector("div[class='JheGif nDgy9d']").text
        excerpt = post.find_element_by_css_selector("div[class='Y3v8qd']").text
        source = post.find_element_by_css_selector("div[class='XTjFC WF4CUc']").text
        date = post.find_element_by_xpath('.//span[@class="WG9SHc"]/span').text
        link = post.find_element_by_xpath('.//a').get_attribute("href")
        article = { 
            "query": main_query,
            "region": main_region,
            "title": title,
            "excerpt": excerpt,
            "date": date,
            "source": source,
            "link": link

        }
        articles.append(article)
    time.sleep(1)

def click_next():
    global status
    try:
        next = driver.find_element_by_id("pnnext")
        next.click()
        status = True
        time.sleep(1)
        print(status)
    except:
        status = False
        print(status)

craft_url('semiconductor','US','1/1/2020','1/31/2020')

while status == True:
    append_articles()
    click_next()

append_articles()

df = pd.DataFrame(articles)
df.to_csv('semiconductor.csv')
