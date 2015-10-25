import sys
import os
import re
import sqlite3
import argparse
from articles import Article, url_pattern

id_pattern = re.compile('.*\?p=(\d+)$')

def find_translation_url(article, lang):
    for url in article.translations.split():
        m = url_pattern.match(url)
        if not m: continue
        l = m.group(1)
        l = 'en' if not l else l[:-1]
        if l == lang:
            return url

def find_translation(article, lang):
    src_url = find_translation_url(article, lang)
    if not src_url: return
    print src_url

def main():
    parser = argparse.ArgumentParser(description='Write articles to disk for alignment')
    parser.add_argument('src_lang', help='source language - original [en]')
    parser.add_argument('trg_lang', help='target language - translated [sw]')
    parser.add_argument('database', help='database path to read articles from')
    args = parser.parse_args()

    conn = sqlite3.connect(args.database)
    trg_cur = conn.cursor()

    trg_cur.execute('select * from articles where lang = ?', (args.trg_lang,))
    for article in trg_cur.fetchall():
       trg_article = Article(*article)
       src_article = find_translation(trg_article, args.src_lang)

if __name__ == '__main__':
    main()
