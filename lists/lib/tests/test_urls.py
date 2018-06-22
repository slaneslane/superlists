import unittest

import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from urls import extract_URLs, URL_2_tagged_link, URL_tagged_text

class ExtractURLsTest(unittest.TestCase):

    def executeTests(self):
        print('Testing module `urls.py` - function: `extract_URLs`')
        self.test_extracting_single_url_from_text_containing_only_url()
        self.test_extracting_single_url_from_full_text()
        self.test_extracting_double_url_from_full_text()

    def test_extracting_single_url_from_text_containing_only_url(self):

        text = 'islane.pl' 
        extracted_url = extract_URLs(text)
        self.assertEqual(len(extracted_url), 1)
        self.assertEqual(extracted_url[0], 'islane.pl')

        text = 'www.islane.pl'
        extracted_www_url = extract_URLs(text)
        self.assertEqual(len(extracted_www_url), 1)
        self.assertEqual(extracted_www_url[0], 'www.islane.pl')

        text = 'http://islane.pl' 
        extracted_http_url = extract_URLs(text)
        self.assertEqual(len(extracted_http_url), 1)
        self.assertEqual(extracted_http_url[0], 'http://islane.pl')

        text = 'http://www.islane.pl'
        extracted_full_url = extract_URLs(text)
        self.assertEqual(len(extracted_full_url), 1)
        self.assertEqual(extracted_full_url[0], 'http://www.islane.pl')

        text = 'https://islane.pl' 
        extracted_https_url = extract_URLs(text)
        self.assertEqual(len(extracted_https_url), 1)
        self.assertEqual(extracted_https_url[0], 'https://islane.pl', )

        text = 'https://www.islane.pl' 
        extracted_full_ssl_url = extract_URLs(text)
        self.assertEqual(len(extracted_full_ssl_url), 1)
        self.assertEqual(extracted_full_ssl_url[0], 'https://www.islane.pl')

        text = 'ftp://www.islane.pl' 
        extracted_ftp = extract_URLs(text)
        self.assertEqual(len(extracted_ftp), 1)
        self.assertEqual(extracted_ftp[0], 'ftp://www.islane.pl')

        text = '12.34.567.89' 
        extracted_numbered_url = extract_URLs(text)
        self.assertEqual(len(extracted_numbered_url), 1)
        self.assertEqual(extracted_numbered_url[0], '12.34.567.89')

        text = 'http://12.34.567.89'
        extracted_http_numbered_url = extract_URLs(text)
        self.assertEqual(len(extracted_http_numbered_url), 1)
        self.assertEqual(extracted_http_numbered_url[0], 'http://12.34.567.89')

        text = '12.34.567.89:98765'
        extracted_numbered_port_url = extract_URLs(text)
        self.assertEqual(len(extracted_numbered_port_url), 1)
        self.assertEqual(extracted_numbered_port_url[0], '12.34.567.89:98765')

        text = 'http://12.34.567.89:98765'
        extracted_http_numbered_port_url = extract_URLs(text)
        self.assertEqual(len(extracted_http_numbered_port_url), 1)
        self.assertEqual(extracted_http_numbered_port_url[0], 'http://12.34.567.89:98765')

        text = 'http://islane.pl/accounts/login?token=87979-56356-53645'
        extracted_tokenized_url = extract_URLs(text)
        self.assertEqual(len(extracted_tokenized_url), 1)
        self.assertEqual(extracted_tokenized_url[0], 'http://islane.pl/accounts/login?token=87979-56356-53645')


    def test_extracting_single_url_from_full_text(self):

        text = 'To jest link do strony: islane.pl - spróbuj!' 
        extracted_url = extract_URLs(text)
        self.assertEqual(len(extracted_url), 1)
        self.assertEqual(extracted_url[0], 'islane.pl')

        text = 'To jest link do strony: www.islane.pl - spróbuj!'
        extracted_www_url = extract_URLs(text)
        self.assertEqual(len(extracted_www_url), 1)
        self.assertEqual(extracted_www_url[0], 'www.islane.pl')

        text = 'To jest link do strony: http://islane.pl - spróbuj!' 
        extracted_http_url = extract_URLs(text)
        self.assertEqual(len(extracted_http_url), 1)
        self.assertEqual(extracted_http_url[0], 'http://islane.pl')

        text = 'To jest link do strony: http://www.islane.pl - spróbuj!'
        extracted_full_url = extract_URLs(text)
        self.assertEqual(len(extracted_full_url), 1)
        self.assertEqual(extracted_full_url[0], 'http://www.islane.pl')

        text = 'To jest link do strony: https://islane.pl - spróbuj!' 
        extracted_https_url = extract_URLs(text)
        self.assertEqual(len(extracted_https_url), 1)
        self.assertEqual(extracted_https_url[0], 'https://islane.pl', )

        text = 'To jest link do strony: https://www.islane.pl - spróbuj!' 
        extracted_full_ssl_url = extract_URLs(text)
        self.assertEqual(len(extracted_full_ssl_url), 1)
        self.assertEqual(extracted_full_ssl_url[0], 'https://www.islane.pl')

        text = 'To jest link do strony: ftp://www.islane.pl - spróbuj!' 
        extracted_ftp = extract_URLs(text)
        self.assertEqual(len(extracted_ftp), 1)
        self.assertEqual(extracted_ftp[0], 'ftp://www.islane.pl')

        text = 'To jest link do strony: 12.34.567.89 - spróbuj!' 
        extracted_numbered_url = extract_URLs(text)
        self.assertEqual(len(extracted_numbered_url), 1)
        self.assertEqual(extracted_numbered_url[0], '12.34.567.89')

        text = 'To jest link do strony: http://12.34.567.89 - spróbuj!'
        extracted_http_numbered_url = extract_URLs(text)
        self.assertEqual(len(extracted_http_numbered_url), 1)
        self.assertEqual(extracted_http_numbered_url[0], 'http://12.34.567.89')

        text = 'To jest link do strony: 12.34.567.89:98765 - spróbuj!'
        extracted_numbered_port_url = extract_URLs(text)
        self.assertEqual(len(extracted_numbered_port_url), 1)
        self.assertEqual(extracted_numbered_port_url[0], '12.34.567.89:98765')

        text = 'To jest link do strony: http://12.34.567.89:98765 - spróbuj!'
        extracted_http_numbered_port_url = extract_URLs(text)
        self.assertEqual(len(extracted_http_numbered_port_url), 1)
        self.assertEqual(extracted_http_numbered_port_url[0], 'http://12.34.567.89:98765')       

        text = 'To jest link do strony: http://islane.pl/accounts/login?token=87979-56356-53645 - spróbuj!'
        extracted_tokenized_url = extract_URLs(text)
        self.assertEqual(len(extracted_tokenized_url), 1)
        self.assertEqual(extracted_tokenized_url[0], 'http://islane.pl/accounts/login?token=87979-56356-53645')


    def test_extracting_double_url_from_full_text(self):

        text = 'To jest link do strony: islane.pl - spróbuj www.test.com.pl !' 
        extracted_url = extract_URLs(text)
        self.assertEqual(len(extracted_url), 2)
        self.assertEqual(extracted_url[0], 'islane.pl')
        self.assertEqual(extracted_url[1], 'www.test.com.pl')

        text = 'To jest link do strony: www.islane.pl - spróbuj www.test.com.pl !'
        extracted_www_url = extract_URLs(text)
        self.assertEqual(len(extracted_www_url), 2)
        self.assertEqual(extracted_www_url[0], 'www.islane.pl')
        self.assertEqual(extracted_www_url[1], 'www.test.com.pl')

        text = 'To jest link do strony: http://islane.pl - spróbuj www.test.com.pl !' 
        extracted_http_url = extract_URLs(text)
        self.assertEqual(len(extracted_http_url), 2)
        self.assertEqual(extracted_http_url[0], 'http://islane.pl')
        self.assertEqual(extracted_http_url[1], 'www.test.com.pl')

        text = 'To jest link do strony: http://www.islane.pl - spróbuj www.test.com.pl !'
        extracted_full_url = extract_URLs(text)
        self.assertEqual(len(extracted_full_url), 2)
        self.assertEqual(extracted_full_url[0], 'http://www.islane.pl')
        self.assertEqual(extracted_full_url[1], 'www.test.com.pl')

        text = 'To jest link do strony: https://islane.pl - spróbuj www.test.com.pl !' 
        extracted_https_url = extract_URLs(text)
        self.assertEqual(len(extracted_https_url), 2)
        self.assertEqual(extracted_https_url[0], 'https://islane.pl')
        self.assertEqual(extracted_https_url[1], 'www.test.com.pl')

        text = 'To jest link do strony: https://www.islane.pl - spróbuj www.test.com.pl !' 
        extracted_full_ssl_url = extract_URLs(text)
        self.assertEqual(len(extracted_full_ssl_url), 2)
        self.assertEqual(extracted_full_ssl_url[0], 'https://www.islane.pl')
        self.assertEqual(extracted_full_ssl_url[1], 'www.test.com.pl')

        text = 'To jest link do strony: ftp://www.islane.pl - spróbuj www.test.com.pl !' 
        extracted_ftp = extract_URLs(text)
        self.assertEqual(len(extracted_ftp), 2)
        self.assertEqual(extracted_ftp[0], 'ftp://www.islane.pl')
        self.assertEqual(extracted_ftp[1], 'www.test.com.pl')

        text = 'To jest link do strony: 12.34.567.89 - spróbuj www.test.com.pl !' 
        extracted_numbered_url = extract_URLs(text)
        self.assertEqual(len(extracted_numbered_url), 2)
        self.assertEqual(extracted_numbered_url[0], '12.34.567.89')
        self.assertEqual(extracted_numbered_url[1], 'www.test.com.pl')

        text = 'To jest link do strony: http://12.34.567.89 - spróbuj www.test.com.pl !'
        extracted_http_numbered_url = extract_URLs(text)
        self.assertEqual(len(extracted_http_numbered_url), 2)
        self.assertEqual(extracted_http_numbered_url[0], 'http://12.34.567.89')
        self.assertEqual(extracted_http_numbered_url[1], 'www.test.com.pl')

        text = 'To jest link do strony: 12.34.567.89:98765 - spróbuj www.test.com.pl !'
        extracted_numbered_port_url = extract_URLs(text)
        self.assertEqual(len(extracted_numbered_port_url), 2)
        self.assertEqual(extracted_numbered_port_url[0], '12.34.567.89:98765')
        self.assertEqual(extracted_numbered_port_url[1], 'www.test.com.pl')

        text = 'To jest link do strony: http://12.34.567.89:98765 - spróbuj www.test.com.pl !'
        extracted_http_numbered_port_url = extract_URLs(text)
        self.assertEqual(len(extracted_http_numbered_port_url), 2)
        self.assertEqual(extracted_http_numbered_port_url[0], 'http://12.34.567.89:98765')       
        self.assertEqual(extracted_http_numbered_port_url[1], 'www.test.com.pl')       

        text = 'To jest link do strony: http://islane.pl/accounts/login?token=87979-56356-53645 - spróbuj www.test.com.pl !'
        extracted_tokenized_url = extract_URLs(text)
        self.assertEqual(len(extracted_tokenized_url), 2)
        self.assertEqual(extracted_tokenized_url[0], 'http://islane.pl/accounts/login?token=87979-56356-53645')
        self.assertEqual(extracted_tokenized_url[1], 'www.test.com.pl')


class URL2TaggedLinkTest(unittest.TestCase):

    def executeTests(self):
        print('Testing module `urls.py` - function: `URL_2_tagged_link`')
        self.test_TaggingURL2Link()

    def test_TaggingURL2Link(self):

        text = 'To jest link do strony: islane.pl - spróbuj!'
        url = 'islane.pl'
        self.assertEqual(URL_2_tagged_link(text, url), 'To jest link do strony: <a target="_blank" href="islane.pl">islane.pl</a> - spróbuj!')

        text = 'To jest link do strony: www.islane.pl - spróbuj!'
        url = 'www.islane.pl'

        text = 'To jest link do strony: http://islane.pl - spróbuj!' 
        url = 'http://islane.pl'

        text = 'To jest link do strony: http://www.islane.pl - spróbuj!'
        url = 'http://www.islane.pl'

        text = 'To jest link do strony: https://islane.pl - spróbuj!' 
        url = 'https://islane.pl'

        text = 'To jest link do strony: https://www.islane.pl - spróbuj!' 
        url = 'https://www.islane.pl'

        text = 'To jest link do strony: ftp://www.islane.pl - spróbuj!' 
        url = 'ftp://www.islane.pl'

        text = 'To jest link do strony: 12.34.567.89 - spróbuj!' 
        url = '12.34.567.89'

        text = 'To jest link do strony: http://12.34.567.89 - spróbuj!'
        url = 'http://12.34.567.89'

        text = 'To jest link do strony: 12.34.567.89:98765 - spróbuj!'
        url = '12.34.567.89:98765'

        text = 'To jest link do strony: http://12.34.567.89:98765 - spróbuj!'
        url = 'http://12.34.567.89:98765'

        text = 'To jest link do strony: http://islane.pl/accounts/login?token=87979-56356-53645 - spróbuj!'
        url = 'http://islane.pl/accounts/login?token=87979-56356-53645'


def main():
    extractURLsTest = ExtractURLsTest()
    extractURLsTest.executeTests()

    url2TaggedLinkTest = URL2TaggedLinkTest()
    url2TaggedLinkTest.executeTests()

if __name__ ==  '__main__':
    main()
