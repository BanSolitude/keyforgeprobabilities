# Heavily based on Tyrox1/Keyforge-Downloader GNU GPL 3.0

import http.cookiejar
import urllib.request
import json
from urllib.error import HTTPError

# TODO read in a start and end page to read decks from.
# TODO get info about mavericks as well

cj = http.cookiejar.CookieJar()  # for handling all the cookies
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
opener.addheaders = [("User-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64;)")]

r = opener.open("https://www.keyforgegame.com/")  # to get all the cookies

deck_dict = {'_metadata': {}, 'data': {}}
page_counter = 1

try:
    with open('KeyforgeDecks.json', 'r') as in_f:
        deck_dict = json.load(in_f)
    page_counter = deck_dict['_metadata']['finish_page']
except FileNotFoundError:
    pass

while page_counter < 1000:
    try:
        r = opener.open("https://www.keyforgegame.com/api/decks/?page=" + str(
            page_counter) + "&links=cards")  # load a list of decks including links to all the cards
    except (HTTPError, ConnectionResetError, KeyboardInterrupt):
        # just output what we have so far when it complains.
        break
    raw = r.read()

    data = json.loads(raw)

    for deck in data['data']:
        deck_id = deck.pop('id', '')
        deck_dict['data'][deck_id] = deck["_links"]["cards"]

    # make this optional?
    for card in data["_linked"]["cards"]:  # get the info for every card
        is_mav = card.pop('is_maverick', False)
        if is_mav:
            with open('Mavericks.json', 'a+') as mav_f:
                json.dump({'card_title': card['card_title'], 'house': card['house']}, mav_f)

    page_counter += 1

deck_dict['_metadata']['finish_page'] = page_counter

with open('KeyforgeDecks.json', 'w+') as out_f:
    json.dump(deck_dict, out_f)
