NotablePeopleCrawler
====================
This program crawls people by profession from [English Wikipedia](http://en.wikipedia.org/).


Motivation
--------------------
We are building a Profiler ([Demo](http://zdev.us/profiler/pro/split.html)) which collects 3 million, and counting, entities with its context. Now that we have a lot of data, we want to build some useful application on top of it. Two of them, namely [EntityTyper](https://github.com/zfei/EntityTyper) and [ProfessionCluterer](https://github.com/zfei/ProfessionClusterer), need sufficient training data. After some research, it seems [this wikipedia list](http://en.wikipedia.org/wiki/Lists_of_people_by_occupation) is a good source.

However, one can easily find that wiki pages are surprisingly unstructured/unfriendly-to-machines. Some list items are in table, some are in data list, some are in ordered list or unordered list, others scatter in text. It's also hard to distinguish between people's pages and irrelevant pages. I implemented some heuristics that gets most of the links that I want.


Features
--------------------
* Automatically crawls people (name + link) in around 180 professions listed in Wikipedia.
* Tries different combinations of list and item tags for people entries (yes, there are cases where a person is in an &lt;li&gt; wrapped inside a &lt;table&gt;), and determines whether the list is relevant based on sibling headers (they sometimes use &lt;p&gt; as a header).
* Keeps visited links and limits a max depth when crawling.


Usage
--------------------
+ For immediate use, you can directly download out.json
+ You can modify/customize crawling heuristics to achieve better performance. For reference, please check out main.py and documentation in the module.
+ To use the module, you will need the following dependencies:
    - BeautifulSoup4 for DOM traversal
    - Html5lib for parsing HTML


License
--------------------
This program is developed for [Cogcomp at University of Illinois](http://cogcomp.cs.illinois.edu/). Therefore it's subject to [Illinois Open Source License](http://otm.illinois.edu/uiuc_openSource).