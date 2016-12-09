import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import BernoulliNB
from sklearn.model_selection import cross_val_score
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

email_path = './beck-s'
new_line = '\n'

def read_email_files(path):
    email_files = []
    for root, dirnames, filenames in os.walk(path):
        email_files.extend([os.path.join(root, f) for f in filenames])
    
    for email_file in email_files:
        with open(email_file) as f:
            lines = f.readlines()
            try:
                body_start = lines.index(new_line)
            except ValueError:
                continue
            body = ''.join(lines[body_start + 1:])
            yield email_file, body

def download_unzip(email_type, urls):
    if not os.path.exists(email_type):
        os.mkdir(email_type)
    cwd = os.getcwd()
    os.chdir(email_type)
    for url in urls:
        fname = url[url.rfind('/') + 1:]
        dirname = fname[:fname.find('.')]
        if os.path.exists(dirname):
            continue
        os.system('wget %s' % url)
        os.system('tar -xzvf %s && rm %s' % (fname, fname))
    os.chdir(cwd)

def read_enron_email_files():
    url = 'http://www.aueb.gr/users/ion/data/enron-spam/'
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    li_tags = soup.find_all('li')
    ham = filter(lambda s : s.strings.next().startswith('ham'), li_tags)[0]
    spam = filter(lambda s : s.strings.next().startswith('spam'), li_tags)[0]
    ham_urls = [t.a.attrs['href'] for t in ham.find_all('li')]
    spam_urls = [t.a.attrs['href'] for t in spam.find_all('li')]
    download_unzip('ham', ham_urls)
    download_unzip('spam', spam_urls)

    index = []
    emails = []
    for fname, body in read_email_files('ham'):
        index.append(fname)
        emails.append(body)

    ham = pd.DataFrame({'body':emails, 'spam': False})
    ham.index = index

    index = []
    emails = []
    for fname, body in read_email_files('spam'):
        index.append(fname)
        emails.append(body)

    spam = pd.DataFrame({'body':emails, 'spam': True})
    spam.index = index


    pd.options.display.expand_frame_repr = False
    df = pd.concat([ham, spam])
    return df.reindex(np.random.permutation(df.index))

df = read_enron_email_files()

cv = CountVectorizer(decode_error='replace')
nb = BernoulliNB()
pl = Pipeline([('cv', cv), ('nb', nb)])

#pl.fit(df.body.values[:1000], df.spam.values[:1000].astype(int))
X = df.body
y = df.spam.astype(int)
print cross_val_score(pl, X[:10000], y[:10000])
