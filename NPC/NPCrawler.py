__author__ = 'zfei'

import urllib2
from bs4 import BeautifulSoup


class Crawler:
    BASE_URL = 'http://en.wikipedia.org'

    def __init__(self, entry_url='/wiki/Lists_of_people_by_occupation'):
        self.visited_links = set()
        self.list_links = self.fetch_lists(entry_url)

    def get_html(self, url):
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        try:
            response = opener.open(self.BASE_URL + url)
            return response.read()
        except (httplib.InvalidURL, urllib2.HTTPError, HTMLParser.HTMLParseError) as e:
            return None

    def get_bs(self, url):
        return BeautifulSoup(self.get_html(url))

    def get_list_name(self, url):
        wiki_free = url.split('/wiki/').pop()
        list_free = wiki_free.split('List_of_').pop()
        lists_free = list_free.split('Lists_of_').pop()
        anchor_free = lists_free.split('#')[0]
        return anchor_free.lower()

    def fetch_lists(self, entry_url):
        self.visited_links.add(entry_url)
        soup = self.get_bs(entry_url)
        list_ul = soup.find(class_='mw-content-ltr').ul  # get list of lists
        list_links = {}
        for li in list_ul.find_all('li'):
            a = li.a
            if not a:
                continue
            list_link = a.get('href')
            if list_link.startswith('/wiki/'):
                list_links[self.get_list_name(list_link)] = list_link
        return list_links

    def get_lists(self):
        return self.list_links

    def get_sibling_list_after_element_with_id(self, page_soup, element_id):
        element = page_soup.find(id=element_id)
        people = {}
        if element:
            people_ul = element.parent.find_next_sibling()
            if people_ul:
                for li in people_ul.find_all('li'):
                    try:
                        people[li.a.text] = self.BASE_URL + li.a.get('href')
                    except AttributeError:
                        pass
        return people

    def get_people_from_tag(self, page_soup, list_tag, item_tag, depth):
        all_lists = page_soup.find(class_='mw-content-ltr').find_all(list_tag)
        people = {}
        for list_tag in all_lists:
            header = list_tag.find_previous_sibling()
            if not header:
                header = list_tag.parent.find_previous_sibling()
            if header and not header.name in ['h2', 'h3', 'p']:
                continue
            if header and not header.find(id='External_links') and not header.find(id='References'):
                for li in list_tag.find_all(item_tag):
                    try:
                        [s.extract() for s in li.find_all('span')]
                        candidate_link = li.a.get('href')
                        if not '/wiki/' in candidate_link:
                            continue
                        if not 'List_of' in candidate_link and not header.find(id='See_also'):
                            people[li.a.text] = self.BASE_URL + candidate_link
                        elif not candidate_link in self.list_links.items() + list(self.visited_links):
                            people.update(self.get_people_from_page(candidate_link, depth - 1))
                        self.visited_links.add(candidate_link)
                    except AttributeError:
                        pass
        return people

    def get_people(self, page_soup, depth):
        result = self.get_people_from_tag(page_soup, 'ul', 'li', depth)
        result.update(self.get_people_from_tag(page_soup, 'ol', 'li', depth))
        result.update(self.get_people_from_tag(page_soup, 'dl', 'dd', depth))
        result.update(self.get_people_from_tag(page_soup, 'table', 'li', depth))
        result.update(self.get_people_from_tag(page_soup, 'table', 'tr', depth))
        return result

    def get_people_from_page(self, page_url, depth):
        if depth <= 0:
            return {}
        page_soup = self.get_bs(page_url)
        if page_soup is None:
            return {}
        [s.extract() for s in page_soup.find_all(class_='thumb')]
        [s.extract() for s in page_soup.find_all(class_='dablink')]
        [s.extract() for s in page_soup.find_all(class_='plainlinks')]
        people = self.get_people(page_soup, depth)
        return people


if __name__ == '__main__':
    my_crawler = Crawler()
    # list_links = my_crawler.get_lists()
    # import pprint
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(list_links)
    # print len(list_links)
    print my_crawler.get_people_from_page('/wiki/List_of_electrical_engineers', 3)
