# Heavily based on Tyrox1/Keyforge-Downloader GNU GPL 3.0

import http.cookiejar
import urllib.request
import json

cj = http.cookiejar.CookieJar()  # for handling all the cookies
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
opener.addheaders = [("User-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64;)")]

r = opener.open("https://www.keyforgegame.com/")  # to get all the cookies

page_counter = 1
card_dict = {}
while len(card_dict) < 370:  # currently there are 370 released cards
    r = opener.open("https://www.keyforgegame.com/api/decks/?page=" + str(
        page_counter) + "&links=cards")  # load a list of decks including links to all the cards
    decks_raw = r.read()

    decks = json.loads(decks_raw)

    for card in decks["_linked"]["cards"]:  # get the info for every card
        is_mav = card.pop('is_maverick', False)
        if not is_mav:
            card_id = card.pop('id', None)
            card_dict[card_id] = card

    print(f"After page {page_counter} there are {len(card_dict)} cards catalogued so far.")
    page_counter += 1

with open('KeyforgeCards.json', 'w') as f:
    json.dump(card_dict, f)
