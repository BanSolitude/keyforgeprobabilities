import json

from datetime import datetime

with open('CardCounts.json', 'r') as in_f:
    card_dict = json.load(in_f)['data']

sorted_by_count = sorted(card_dict.values(), key=lambda x: x['count'], reverse=True)

with open(f"KeyforgeCardStats{datetime.now().strftime('%y%W%w%H%M%S')}.txt", "w+") as out_f:
    rarity_count = {'Common': 0,
                    'Uncommon': 0,
                    'Rare': 0,
                    'Variant': 0,
                    'FIXED': 0,
                    'Maverick': 0}
    for card in sorted_by_count:
        rarity_count[card['r']] += card['c']
        out_f.write(f"Found {card['c']} copies of {card['n']}\n")
    out_f.write("\n")
    out_f.write(f"Found {rarity_count['Maverick']} mavericks\n")
    out_f.write("\n")
    out_f.write(f"There were {rarity_count['Common']} commons, {rarity_count['Uncommon']} uncommons, and\
        {rarity_count['Rare']} rares.\n")
    out_f.write(f"Additionally there were {rarity_count['FIXED']} cards whose presence is fixed to another card\
        appearing, and {rarity_count['Variant']} cards which cannot appear with some other card.\n")
