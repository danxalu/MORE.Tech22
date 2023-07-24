from bs4 import BeautifulSoup
import requests
import json
import aiohttp
import asyncio

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36 Edg/106.0.1370.34"
    }

dataTitles = [] #кортеж новостей
data = []

async def get_page_data(session, page, name_smi, scr, tag, main_class, child_cond_tag = '', child_cond_class = ''):
    url = scr.format(page) #url текущей страницы
    async with session.get(url=url.format(name_smi, page), headers=headers) as response:
        response_text = await response.text() #получаем содердимое страницы
        soup = BeautifulSoup(response_text, 'html.parser')

        #with open(url, 'w', encoding='utf-8') as fp: #
            #fp.write(str(soup)) #скачиваем страницу
            
        global news
        if child_cond_tag != '': #дополнительное условие для вычленения новостей из страницы
            inf = soup.find_all(tag, class_ = main_class)
            for x in inf:
                news = x.findChildren(child_cond_tag, class_ = child_cond_class)
        else:
            news = soup.find_all(tag, class_ = main_class) #ищем все элементы с данными тэгом и классом

        current_scr = ""
        for one_news in news:
            current_str = one_news.text.strip() #выделяем новость
            current_str = throw_rush(current_str)

            if(tag == "a"): #если это тег a, то извлекаем ссылку на новость
                current_scr = one_news.attrs.get("href")
                if current_scr[0]=="/": #если ссылка неполная, дополняем ее доменом
                    current_scr = "http://" + name_smi + current_scr
                    
            else: #если это не тег a, ищем родителя/ребёнка с ссылкой
                parent_news = one_news.find_parents("a") #
                if parent_news:
                    current_scr = parent_news[0].attrs.get("href")
                else:
                    children_news = one_news.findChildren("a")
                    if children_news:
                        current_scr = children_news[0].attrs.get("href")
                if current_scr and current_scr[0]=="/":
                    current_scr = "http://" + name_smi + current_scr
            dataTitles.append(current_str)
            data.append([current_str, current_scr])

async def gather_data(name_smi, count_pages_news, scr, tag, main_class, parent_cond_tag = '', parent_cond_class = ''): #сбор новостей
    async with aiohttp.ClientSession() as session:
        tasks = []
        for page in range(1, count_pages_news+1):
            task = asyncio.create_task(get_page_data(session, page, name_smi, scr, tag, main_class, parent_cond_tag, parent_cond_class))
            tasks.append(task)
        await asyncio.gather(*tasks)
        print(name_smi, "-- done")

def parse_smi(name_smi, count_pages_news, scr, tag, main_class, parent_cond_tag = '', parent_cond_class = ''): #функция запуска парсинга
    asyncio.run(gather_data(name_smi, count_pages_news, scr, tag, main_class, parent_cond_tag, parent_cond_class))

def to_json(bases, name_file): #экспорт в json
    with open("{0}.json".format(name_file), "w", encoding='utf-8') as file:
        json.dump(bases, file, indent=4, ensure_ascii=False)

def throw_rush(into):
    for k in range(0, 10):
        q = "\n"+str(k)+"\n"
        into = into.replace(q," ")
    q = "\n"+str(k)+"\n"
    into = into.replace("\n\n"," ")
    into = into.replace("\n"," ")
    into = into.replace("\r",'')
    into = into.replace('\"','')
    return into
        
        
if __name__ == '__main__':
    parse_smi('kommersant.ru', 2, 'https://www.kommersant.ru/lenta?from=all_lenta&page={0}', 'a', 'uho__link uho__link--overlay')
    parse_smi('glavkniga.ru', 2, 'https://glavkniga.ru/news/filter?&p={0}', 'a', 'news_block_hdg')
    parse_smi('e-xecutive.ru', 2, 'https://www.e-xecutive.ru/sections/hr-news/news?page={0}', 'a', 'news-half__title')
    to_json(data, "news")
    to_json(dataTitles, "newsTitles")
