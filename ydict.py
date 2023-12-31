#!/bin/python
'''
Python script will look up definitions of pasted words into youdao.com and return definition listing.
'''

from ydict_lib import ylib


def view(defn_dict: dict) -> None:
    '''Display colorized definitions page.'''
    title_txt = ylib.console_color_fmt(input_str=defn_dict['title'], color_str='red')
    print(title_txt)

    phonetic_txt = ylib.console_color_fmt(input_str=f"({defn_dict['phonetic']})", color_str='yellow')
    print(phonetic_txt)

    for defn in defn_dict['dict_book']:
        txt = ylib.console_color_fmt(input_str=defn, color_str='green')
        print(txt)


def main() -> None:
    while True:
        lookup_str = input('ydict: ')

        if lookup_str.lower() == 'q':
            break

        # Get the definitions
        try:
            yd_html = ylib.yd_lookup(input_str=lookup_str)
        except AssertionError:
            continue

        yd_defn = ylib.parse_html_from_response(yd_html)

        # Start printing the outputs
        view(yd_defn)


if __name__ == "__main__":
    main()
