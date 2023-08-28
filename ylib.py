import requests
from bs4 import BeautifulSoup
import re


def console_color_fmt(input_str: str, color_str: str = 'off') -> str:
    '''
    Produces a temporary string formatter display strings in the console with selected color.

    Source URL: https://blog.csdn.net/weixin_38314865/article/details/104304957

    Parameters
    ----------
    input_str:
        String to format
    color_str: str = 'off'
        Definition of colors. Available colors include:

        - black
        - red
        - green
        - yellow
        - blue
        - magenta
        - cyan
        - white
		
		Set to 'off' (default) to turn off formatting.

    Returns
    -------
    fmt_string: str
        Input string with the color code required for terminal display.
    '''

    color_fmt = {
            'black': '\033[0;30m',
            'red': '\033[0;31m',
            'green': '\033[0;32m',
            'yellow': '\033[0;33m',
            'blue': '\033[0;34m',
            'magenta': '\033[0;35m',
            'cyan': '\033[0;36m',
            'white': '\033[0;37m',
            'off': '\033[0m',
            }

    selected_color = color_fmt[color_str]
    end_selected_color = color_fmt['off']

    return f'{selected_color}{input_str}{end_selected_color}'


def yd_lookup(input_str: str) -> requests.Response:
    '''
    Scrape raw website data from youdao, given the input to look up.

    Parameters
    ----------
    input_str: str
        String to look up on youdao.

    Returns
    -------
    page
        Return the requests.Response object handle to the provided URL
    '''
    # Generate the URL to obtain the definition
    url = f'https://youdao.com/result?word={input_str}&lang=en'

    # Download the html contents from the above url
    page = requests.get(url)
    return page


def parse_html_from_response(request_response: requests.Response) -> dict:
    '''
    Parse the returned response handle's HTML to obtain components such as definition, phonetics and examples.
	
	Parameters
	----------
	requests_response: requests.Response
		Requests object after parsing URL
	
	Returns
	-------
	extract: dict
		Parse results including:
		
		1. title: the word being searched
		2. phonetic: phonetics of the word
		3. dict_book: List of all the definitions given
	
		titles of the dictionary reflect the HTML tags for youdao.
    '''
    page = request_response
    soup = BeautifulSoup(page.content, 'html.parser')

    defn_items = {}
    result_dump = soup.find(id='searchLayout')

    # Items in dictionary correspond the the tags in the HTML code

    # Title: Name of string found
    title_txt = result_dump.find('div', class_='title').text
    title_end = title_txt.find('语')
    defn_items['title'] = title_txt[:title_end]

    # Phonetics: The phonetics for the word looked up
    try:
        phonetic_text = result_dump.find('span', class_='phonetic').text
        defn_items['phonetic'] = phonetic_text.replace('/', '')
    except AttributeError:  # Some items do not return a phonetic text, so leave this blank
        defn_items['phonetic'] = ''

    # Dictionary definitions, dependent on language
    defn_htmls_en = result_dump.find_all('li', class_='word-exp')
    defn_htmls = result_dump.find_all('div', class_='word-exp')

    defns = []
    for i in range(len(defn_htmls)):
        defn_html = defn_htmls[i]

        if i == 0:
            if len(defn_htmls_en) == 0:
                defns.append(f'Definition:\t{defn_html.text}')
            else:
                defns.append(f'Definition:\t{defn_htmls_en[0].text}')
                defns.append(f'\t{defn_html.text}')
            continue

        defns.append(f'\t{defn_html.text}')

    defn_items['dict_book'] = defns

    return defn_items
