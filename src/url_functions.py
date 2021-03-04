from bs4 import BeautifulSoup
import requests
from tqdm import tqdm


def get_content_(url):
    """
    Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
    Accept-Encoding:gzip, deflate, sdch
    Accept-Language:en-US,en;q=0.8,vi;q=0.6
    Connection:keep-alive
    Cookie:__ltmc=225808911; __ltmb=225808911.202893004; __ltma=225808911.202893004.204252493; _gat=1; __RC=4; __R=1; _ga=GA1.3.938565844.1476219934; __IP=20217561; __UF=-1; __uif=__ui%3A-1%7C__uid%3A877575904920217840%7C__create%3A1475759049; __tb=0; _a3rd1467367343=0-9
    Host:dantri.com.vn
    Referer:http://dantri.com.vn/su-kien.htm
    Upgrade-Insecure-Requests:1
    User-Agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36
    """
    domain = None
    domains = url.split('/')
    if (domains.__len__() >= 3):
        domain = domains[2]

    headers = dict()
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    headers['Accept-Encoding'] = 'gzip, deflate, sdch'
    headers['Accept-Language'] = 'en-US,en;q=0.8,vi;q=0.6'
    headers['Connection'] = 'keep-alive'
    headers['Host'] = domain
    headers['Referer'] = url
    headers['Upgrade-Insecure-Requests'] = '1'
    headers[
        'User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'

    r = requests.get(url, headers=headers, timeout=10)
    r.encoding = 'utf-8'
    r.close()
    return str(r.text)


def get_content_news_from_news_url(url: str) -> dict:
    """
    Example Args:
        url: 'https://vnexpress.net/brazil-nguy-co-thanh-lo-ap-bien-chung-ncov-4242061.html'

    Returns:
        a dictionary includes:
            - title
            - description
            - contents
            - url
    """
    try:
        raw_content = get_content_(url)
        soup = BeautifulSoup(raw_content, 'html.parser')

        title_detail = soup.find("h1", class_="title-detail").text

        description = soup.find("p", class_="description").text

        # lay noi dung bai bao
        content_text = ""
        for div_bodymain in soup.find_all("article", class_="fck_detail"):
            for p_element in div_bodymain.find_all('p', 'Normal'):
                content_text += p_element.text
        if len(content_text) < 10:
            return None
        return {
            "title": title_detail,
            "description": description,
            "contents": content_text,
            "url": url
        }
    except Exception:
        return None


def get_news_links_from_sub_topic_page_link(sub_topic_page_link: str) -> list:
    """Get all links of news given the link of a page of a topic
    Example Args:
        topic_link: 'https://vnexpress.net/the-gioi/tu-lieu-p1'

    Returns:
        list of links
    """
    links = []
    raw_content = get_content_(sub_topic_page_link)
    soup = BeautifulSoup(raw_content, 'html.parser')
    for article in soup.find_all("article"):
        try:
            p = article.find('h2', class_='title-news')
            url = p.find('a', href=True)
            links.append(url['href'])
        except Exception:
            # print(e)
            pass
    return links


def get_page_urls_from_sub_topic_url(sub_topic_url, pages=1) -> list:
    """Get urls for vnexpress categories. Each category may span hundreds of pages.
    """

    urls = []
    urls.append(sub_topic_url)
    for page in range(1, pages, 1):
        urls.append(sub_topic_url + f"-p{page}")

    return urls


def get_all_news_urls_from_topics_links(topics_links: dict, n_pages_per_topic=1) -> dict:
    """Get links to the news for each topics given a list of links to list of topics

    Eaxmple Args:
        topics_links: {
            'thoi-su': [
                'https://vnexpress.net/thoi-su',
                'https://vnexpress.net/chinh-tri',
            ],
            ....
        }

    Returns:
        {
            'thoi-su': [
                'https://vnexpress.net/lap-184-don-vi-bau-cu-dai-bieu-quoc-hoi-tren-toan-quoc-4243509.html',
                ...
            ],
            ....
        }
    """
    output = {}
    for k, v in tqdm(topics_links.items()):
        print(f'topic: {k} - No.sub_topics: {len(v)}')
        output[k] = []
        page_links = []
        for sub_topic_link in tqdm(v):
            s = get_page_urls_from_sub_topic_url(sub_topic_link, pages=n_pages_per_topic)
            page_links = page_links + s
        for page_link in tqdm(page_links):
            news_links = get_news_links_from_sub_topic_page_link(page_link)
            output[k] = output[k] + news_links
    return output
