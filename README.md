NotablePeopleCrawler
====================
This program crawls people by profession from [English Wikipedia](http://en.wikipedia.org/)

Why bother?
--------------------
I have written a ['Profiler'](http://zdev.us/profiler/pro/split.html) which collects 3 million and counting entities with its context. Now that we have a lot of data, we want to build some useful application on top of it. Two of them, namely [EntityTyper](https://github.com/zfei/EntityTyper) and [ProfessionCluterer](https://github.com/zfei/ProfessionClusterer), need some training data. After some research, it seems [this wikipedia list](http://en.wikipedia.org/wiki/Lists_of_people_by_occupation) is a good source.

However, one can find wiki pages are surprisingly unstructured/unfriendly-to-mechines. Some lists are in table, some are in data list, others in ordered list or unordered list. It's also hard to distinguish between people's pages and irrelevant pages. I implemented some heuristics and luckily we got most of the links that we want.

License
--------------------
This program is developed for [Cogcomp at University of Illinois](http://cogcomp.cs.illinois.edu/). It's subject to [Illinois Open Source License](http://otm.illinois.edu/uiuc_openSource).