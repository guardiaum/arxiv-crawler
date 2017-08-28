# 2017.08.28 00:05:39 BRT
#Embedded file name: /home/jms5/eclipse-workspace/arxiv-crawler/arxiv-scraper/scraper.py
import scrapy

class ArxivSpider(scrapy.Spider):
    name = 'arxiv_spider'
    start_urls = ['https://arxiv.org/list/cs/new']

    def parse(self, response):
        META_SELECTOR = '.meta'
        
        for arxiv in response.css(META_SELECTOR):
            TITLE_SELECTOR = '.list-title ::text'
            AUTHORS_SELECTOR = '.list-authors a ::text'
            COMMENTS_SELECTOR = './div[@class="list-comments"]/text()'
            JOURNAL_SELECTOR = './div[@class="list-journal-ref"]/text()'
            SUBJECTS_SELECTOR = './div[@class="list-subjects"]//text()'
            ABSTRACT_SELECTOR = './/p[contains(@class, "mathjax")]/text()'
            
            title = (arxiv.css(TITLE_SELECTOR).extract()[2],)
            authors = (arxiv.css(AUTHORS_SELECTOR).extract(),)
            comments = (arxiv.xpath(COMMENTS_SELECTOR).extract(),)
            journal_ref = (arxiv.xpath(JOURNAL_SELECTOR).extract(),)
            subjects = (arxiv.xpath(SUBJECTS_SELECTOR).extract(),)
            abstract = arxiv.xpath(ABSTRACT_SELECTOR).extract()
            
            yield {'title': title,
             'authors': authors,
             'comments': comments,
             'journal-ref': journal_ref,
             'subjects': subjects,
             'abstract': abstract}
            
            if abstract :
		    fileName = title[0].replace('\n', '').replace('/', '')
		    file = open('output/' + fileName.encode('utf-8') + '.txt', 'w')
		    file.write('Title: ')
		    file.write(title[0].encode('utf-8'))
		    file.write('\nAuthors: ')
		    for authorsX in authors:
		        for author in authorsX:
		            file.write(author.encode('utf-8') + ', ')
		        file.write('\n')
		        
		    file.write('\nComments: ')
		    for commentsX in comments:
		        if commentsX:
		            for comment in commentsX:
		                file.write(comment.encode('utf-8'))
		        else:
		            file.write('NA')
		            file.write('\n')
		            
		    file.write('\nJournal-ref: ')
		    for journal_refX in journal_ref:
		        if journal_refX:
		            for journal_ref in journal_refX:
		                file.write(journal_ref.encode('utf-8'))
		        else:
		            file.write('NA')
		            file.write('\n')
		    
		    file.write('\n')
		    for subjectsX in subjects:
		        for subject in subjectsX:
		            file.write(subject.encode('utf-8'))
		            
		    file.write('\nAbstract:')
		    if abstract:
		        for a in abstract:
		            file.write(a.encode('utf-8'))
		    else:
		        file.write('NA')
		        
		    file.close()
