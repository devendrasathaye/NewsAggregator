from bs4 import BeautifulSoup, NavigableString
import requests
from concurrent.futures import ThreadPoolExecutor

request_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/114.0.5735.16 Safari/537.36',
}

sess = requests.session()


class NewsAggregator:
    def __init__(self):
        self.news_hrefs = []
        self.news_channels = {
            'in_timesnow': ["https://www.timesnownews.com/", ["_1D35", "_3znU"]],
            "in_abpnews": ["https://www.abplive.com/", "_top-story-wrap"],
            "in_indiatoday": ['https://www.indiatoday.in/', 'lhs__section'],
            "in_aajtak": ['https://www.aajtak.in/', 'content-area'],
            "in_news18": ["https://www.news18.com", ["jsx-2782b689ab6e802f", "top_story"]]
        }

    @staticmethod
    def get_soup(url):
        try:
            res = sess.get(url, headers=request_headers)
            if res.status_code == 200:
                soup = BeautifulSoup(res.content, 'lxml')
                return soup
        except Exception:
            print('soup failed')
            return None
        return None

    @staticmethod
    def timesnow_news(news_soup):
        h1_tag = news_soup.find('h1', class_="_1Fcx")
        if h1_tag:
            title = h1_tag.text.replace('\n', '').strip()
            tag = h1_tag.parent
            if tag:
                tag = tag.parent
                if tag:
                    if tag.name == 'div':
                        div = tag.find('div', class_='_11eW')
                        content_list = list(set([x.text for x in div.findAll('div') if x]))
                        content = ". ".join([x for x in content_list if len(x) > 20])
                        return title, content
        return '', ''

    @staticmethod
    def abpnews_news(news_soup):
        h1_tag = news_soup.find('h1', class_="abp-article-title")
        if h1_tag:
            title = h1_tag.text.replace('\n', '').strip()
            tag = h1_tag.parent
            if tag:
                if tag.name == 'section':
                    content_list = list(set([x.text for x in tag.children if x.name != 'h1']))
                    content_list = [' '.join([y for y in x.replace('\n', '').split(' ') if y]) for x in content_list]
                    content = ". ".join([x for x in content_list if len(x) > 20])
                    return title, content
        return '', ''

    @staticmethod
    def indiatoday_news(news_soup):
        h1_tag = news_soup.find('h1', class_=["jsx-ace90f4eca22afc7", "Story_strytitle__MYXmR"])
        if h1_tag:
            title = h1_tag.text.replace('\n', '').strip()
            tag = news_soup.find('div',
                                 class_=['jsx-ace90f4eca22afc7', 'Story_description__fq_4S', 'description', 'paywall',
                                         'story-with-main-sec'])
            if tag:
                content_list = list(set([x.text for x in tag.children if x.name != 'h1']))
                content_list = [' '.join([y for y in x.replace('\n', '').split(' ') if y]) for x in content_list]
                content = ". ".join([x for x in content_list if len(x) > 20])
                return title, content
        return '', ''

    @staticmethod
    def aajtak_news(news_soup):
        d = news_soup.find('div', class_="story-heading")
        if d:
            h1_tag = d.find('h1')
            if h1_tag:
                title = h1_tag.text.replace('\n', '').strip()
                tag = news_soup.find('div', class_="story-with-main-sec")
                if tag:
                    if tag.name == 'div':
                        content_list = []
                        for x in tag.children:
                            if x:
                                if x.name != 'h1' and not isinstance(x, NavigableString):
                                    if 'brdcum-fedback-main' not in x.get('class', []):
                                        content_list.append(x.text)
                        content_list = list(set(content_list))
                        content_list = [' '.join([y for y in x.replace('\n', '').split(' ') if y]) for x in
                                        content_list]
                        content = ". ".join([x for x in content_list if len(x) > 20])
                        return title, content
        return '', ''

    @staticmethod
    def news18_news(news_soup):
        h1_tag = news_soup.find('h1', class_=["jsx-926f17af57ac97dc", "article_heading"])
        if h1_tag:
            title = h1_tag.text.replace('\n', '').strip()
            tag = news_soup.find('div', id="article_ContentWrap")
            if tag:
                content_list = []
                for x in tag.findAll('p'):
                    if x.text not in content_list:
                        content_list.append(x.text)
                content_list = list(set(content_list))
                content_list = [' '.join([y for y in x.replace('\n', '').split(' ') if y]) for x in content_list]
                content = ". ".join([x for x in content_list if len(x) > 20])
                return title, content
        return '', ''

    def parse_news(self, href):
        news_soup = self.get_soup(href)
        title = content = ""
        if news_soup:
            if href.startswith('https://www.timesnownews.com/'):
                title, content = self.timesnow_news(news_soup)
            elif href.startswith('https://www.abplive.com/'):
                title, content = self.abpnews_news(news_soup)
            elif href.startswith('https://www.indiatoday.in/'):
                title, content = self.indiatoday_news(news_soup)
            elif href.startswith('https://www.aajtak.in/'):
                title, content = self.aajtak_news(news_soup)
            elif href.startswith('https://www.news18.com'):
                title, content = self.news18_news(news_soup)
            return title, content
        return '', ''

    def main(self):
        news_aggregator = {}
        for news_channel in self.news_channels.keys():
            news = {}
            url, class_ = self.news_channels[news_channel]
            soup = self.get_soup(url)
            if soup:
                div_tag = soup.find('div', class_=class_)
                for a_tag in div_tag.findAll('a'):
                    if a_tag:
                        href = a_tag.get('href', '')
                        if href and 'anchor' not in href:
                            if href.startswith(url):
                                self.news_hrefs.append(href)

                pool = ThreadPoolExecutor(max_workers=10)
                for title, content in pool.map(self.parse_news, self.news_hrefs):
                    if len(content):
                        news[title] = content
                pool.shutdown()
            news_aggregator[news_channel] = news
        return news_aggregator


if "__main__" == __name__:
    news_aggregator = NewsAggregator()
    results = news_aggregator.main()
