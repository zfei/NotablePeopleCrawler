__author__ = 'zfei'

import json
from NPC import NPCrawler


def main():
    my_crawler = NPCrawler.Crawler()

    list_links = my_crawler.get_lists()
    profession_dict = {}
    alpha_count = 0
    for list_name in list_links:
        list_url_suffix = list_links[list_name]
        list_url = my_crawler.BASE_URL + list_url_suffix
        print list_url,
        people_list = my_crawler.get_people_from_page(list_url_suffix, 3)
        print len(people_list)
        if len(people_list) > 0:
            profession_dict[list_name] = people_list
            alpha_count += 1
    print alpha_count
    with open('out.json', 'w') as f:
        f.write(json.dumps(profession_dict))

main()