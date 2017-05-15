import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import urllib
import sqlite3

import countries_database
import strings_database

def update_countries_db(ckey, flag_fname):
    conn = sqlite3.connect('countries.db')
    c = conn.cursor()
    query = u'INSERT INTO countries (ckey, flag) VALUES ("{}", "{}.png");'.format(ckey, flag_fname)
    c.execute(query)
    conn.commit()
    conn.close()


def update_strings_db(skey, wiki_locale_map, names):
    conn = sqlite3.connect('strings.db')
    c = conn.cursor()
    order = wiki_locale_map.keys()
    order = sorted(order)
    locales_columns = u', '.join(order)

    locales_values = u'"' + u'", "'.join(str(names[wiki_locale_map[key]]) for key in order) + u'"'
    query = u'INSERT INTO countries (skey, {}) VALUES ("{}", {});'.format(locales_columns, skey, locales_values)
    c.execute(query)
    conn.commit()
    conn.close()


def flag_and_countrys_urls(url):
    parsed_url = urlparse(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html5lib")
    prefix = u'{}://{}'.format(parsed_url.scheme, parsed_url.netloc)

    for link in soup.findAll('a'):
        if link.get('title') is not None and link.get('href') is not None:
            if 'Flag of ' in link.get('title') and link.get('href').endswith('.svg'):
                flag_td = link.parent
                flag_tr = flag_td.parent
                tbody = flag_tr.parent
                country_url = urljoin(prefix, get_link_country_site(tbody, flag_tr))
                flag_url = urljoin(prefix, link.get('href'))
                yield flag_url, country_url


def get_country_name(country_url):
    '''
    returns downloaded country name from country url
    '''
    r = requests.get(country_url)
    soup = BeautifulSoup(r.text, "html5lib")
    h1_name = soup.find('h1')
    return h1_name.text


def get_locales(country_url):
    langs = set()
    r = requests.get(country_url)
    soup = BeautifulSoup(r.text, "html5lib")
    lang_div = soup.find(id='p-lang')
    for body_div in lang_div.findAll('div'):
        if body_div.get('class') == 'body':
            ul = body_div.find('ul')
            for li in ul.findAll('li'):
                a = li.find('a')
                langs.add(a.get('lang'))
    return langs


def get_country_names_for_locales(country_url, locales, curr_locale):
    country_names = {locale: None for locale in locales}
    r = requests.get(country_url)
    soup = BeautifulSoup(r.text, "html5lib")
    lang_div = soup.find(id='p-lang')
    country_names[curr_locale] = get_country_name(country_url)
    for body_div in lang_div.findAll('div'):
        if body_div.get('class') == 'body':
            ul = body_div.find('ul')
            for li in ul.findAll('li'):
                a = li.find('a')
                if a.get('lang') in locales:
                    country_names[a.get('lang')] = get_country_name(u'https:{}'.format(a.get('href')))
    return country_names

def get_link_country_site(tbody, flag_tr):
    for child_tr in tbody.findAll('tr'):
        if child_tr is not flag_tr:
            # print '\tNie jest :', child_tr
            for link in child_tr.findAll('a'):
                if link.get('title') is not None and link.get('href') is not None:
                    if 'Flag of' not in link.get('title'):
                        return link.get('href')


def get_link_to_image_site(url):
    parsed_url = urlparse(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html5lib")
    prefix = u'{}://{}'.format(parsed_url.scheme, parsed_url.netloc)
    for link in soup.findAll('a'):
        if link.get('title') is not None and link.get('href') is not None:
            if 'Flag of ' in link.get('title') and link.get('href').endswith('.svg'):
                yield urljoin(prefix, link.get('href'))


def get_link_to_svg(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html5lib")
    for link in soup.findAll('a'):
        if link.text is not None:
            if 'Original file' in link.text:
                print(link.text, link.get('href'))
                return u'{}:{}'.format('https', link.get('href'))


def download_file(url):
    r = requests.get(url, stream=True)
    f_name = url.split('/')[-1]
    print(f_name)
    if r.status_code == 200:
        file_path = './flag_pictures/' + f_name
        with open(file_path, 'wb') as f:
            for chunk in r:
                f.write(chunk)
    return f_name


if __name__ == '__main__':
    wiki_locale_map = {'pl_PL': 'pl', 'en_US': 'en'}
    for i, (flag_url, country_url) in enumerate(
            flag_and_countrys_urls('https://en.wikipedia.org/wiki/Gallery_of_sovereign_state_flags')):
        print(i, get_country_name(country_url))
        print(u'\tcountry_url :', country_url)
        print(u'\tflag_url :', flag_url)
        names = get_country_names_for_locales(country_url, ['pl', 'fr'], 'en')
        for loc in [u'pl', u'en', u'fr']:
            print(u'{}: {}'.format(loc, names[loc]))

        svg_flag_url = get_link_to_svg(flag_url)
        flag_fname = download_file(svg_flag_url)
        if flag_fname.endswith(u'.svg'):
            flag_fname = flag_fname[:-4]

        update_countries_db(names[u'en'], flag_fname)
        update_strings_db(names[u'en'], wiki_locale_map, names)
