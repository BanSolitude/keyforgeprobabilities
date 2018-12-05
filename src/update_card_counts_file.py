# Heavily based on Tyrox1/Keyforge-Downloader GNU GPL 3.0

import http.cookiejar
import json
import time
import urllib.request

from urllib.error import HTTPError, URLError

# TODO read in a start and end page to read decks from.
# TODO get info about mavericks as well

cj = http.cookiejar.CookieJar()  # for handling all the cookies
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
opener.addheaders = [("User-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64;)")]

r = opener.open("https://www.keyforgegame.com/")  # to get all the cookies

card_dict = {}
page_counter = 1

try:
    with open('CardCounts.json', 'r') as in_f:
        sup_dict = json.load(in_f)
    page_counter = sup_dict['_metadata']['finish_page']
    last_deck = sup_dict['_metadata']['finish_deck']
    card_dict = sup_dict['data']
except FileNotFoundError:
    with open('KeyforgeCards.json', 'r') as in_f:
        card_db = json.load(in_f)
        for card_id in card_db:
            # TODO set house based on enum rather than string. Maybe rarity too
            card_dict[card_id] = {'n': card_db[card_id]['card_title'], 'r': card_db[card_id]['rarity'],
                                  'h': card_db[card_id]['house'], 'c': 0, 'm': 0}
        card_dict['maverick'] = {'card_title': None, 'rarity': None, 'count': 0}

old_clock = time.clock()
print("Starting at " + str(page_counter))
while True:
    try:
        r = opener.open("https://www.keyforgegame.com/api/decks/?page=" + str(
            page_counter))  # load a list of decks including links to all the cards
    except (HTTPError, ConnectionResetError, KeyboardInterrupt, URLError) as e:
        print(str(e))
        # TODO figure out what deck id we ended on in case we went past the end of the list (HTTP error 404)
        # just output what we have so far when it complains.
        break

    raw_json = r.read()
    parsed_json = json.loads(raw_json)

    decks = parsed_json['data']
    for deck in decks:
        for card_id in deck['cards']:
            if card_id in card_dict:
                card_dict[card_id]['count'] += 1
            else:
                # TODO get card info and update a maverick count on actual card
                card_dict['maverick']['count'] += 1

    page_counter += 1

    clock = time.clock()
    if clock - old_clock > 100:
        old_clock = clock
        print("Currently on page " + str(page_counter))

print("finished on page " + str(page_counter))
with open('CardCounts.json', 'w+') as out_f:
    json.dump({'_metadata': {'finish_page': page_counter}, 'data': card_dict}, out_f)
