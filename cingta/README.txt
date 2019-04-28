#Before you run the cingtaSpider, please install the following 2 modules firstly.
pip install pywin32
pip install goto-statement

cingtaDetailSpider.py is used for detail page debug.
cingtaSpider.py only crawl the following items now:
1. Title
2. URL
3. Date
4. Type
5. Source

How to use:
cd ./cingta
scrapy crawl cingta -o cingtadetail.xml