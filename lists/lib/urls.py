import re

def extract_URLs(text):
    pattern = r'(?:(?:(?:https?|ftp)://))?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!|%\$&\'\(\)\*\+,;=.]+'
    regexp = re.compile(pattern)
    return regexp.findall(text)

def URL_2_tagged_link(text, url):
    url_encoded = url.replace('?', '%3F')
    text_encoded = text.replace(url, url_encoded)
    ahref = '<a target="_blank" href="{0}">{1}</a>'.format(url_encoded, url)
    return re.sub(url_encoded, ahref, text_encoded)

def URL_tagged_text(text):
    urls = extract_URLs(text)
    for url in urls:
        text = URL_2_tagged_link(text, url)
    return text
