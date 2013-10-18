__author__ = 'zfei'

import urllib2
from bs4 import BeautifulSoup
import html5lib


class Crawler:
    BASE_URL = 'http://en.wikipedia.org'

    def __init__(self, entry_url='/wiki/Lists_of_people_by_occupation'):
        self.cached_results = {}
        self.list_links = self.fetch_lists(entry_url)

    def get_html(self, url):
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        try:
            response = opener.open(self.BASE_URL + url)
            return response.read()
        except Exception:
            return None

    def get_bs(self, url):
        try:
            return BeautifulSoup(self.get_html(url), 'html5lib')
        except Exception:
            return None

    def get_list_name(self, url):
        wiki_free = url.split('/wiki/').pop()
        list_free = wiki_free.split('List_of_').pop()
        lists_free = list_free.split('Lists_of_').pop()
        anchor_free = lists_free.split('#')[0]
        return anchor_free.lower()

    def fetch_lists(self, entry_url):
        # self.visited_links.add(entry_url)
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
            if header and not header.name in ['h2', 'h3', 'p', 'dl']:
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
                        # elif not candidate_link in self.list_links.items() + list(self.visited_links):
                        elif not candidate_link in self.list_links.items():
                            people.update(self.get_people_from_page(candidate_link, depth - 1))
                        # self.visited_links.add(candidate_link)
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

    def remove_tags_by_class(self, page_soup, class_name):
        [s.extract() for s in page_soup.find_all(class_=class_name)]

    def remove_irrelevant_tags(self, page_soup):
        irrelevant_tag_classes = [
            'thumb',
            'dablink',
            'plainlinks',
            'noprint',
            'tright',
            'portal',
            'rellink',
            'boilerplate',
            'seealso'
        ]
        for tag_class in irrelevant_tag_classes:
            self.remove_tags_by_class(page_soup,tag_class)

    def get_people_from_page(self, page_url, depth):
        cache_key = str(depth) + page_url
        if cache_key in self.cached_results:
            return self.cached_results[cache_key]
        if depth <= 0:
            return {}
        page_soup = self.get_bs(page_url)
        if page_soup is None:
            # another chance
            print 'error', page_url,
            page_soup = self.get_bs(page_url)
            if page_soup is None:
                print 'error again', page_url,
                return {}
        self.remove_irrelevant_tags(page_soup)
        people = self.get_people(page_soup, depth)
        self.cached_results[cache_key] = people
        return people


if __name__ == '__main__':
    my_crawler = Crawler()
    print len(my_crawler.get_people_from_page('/wiki/Lists_of_scientists', 3).items())
