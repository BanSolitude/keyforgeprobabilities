TOTAL_COMB = 35.0

PNumHouses = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0]]

e = .0000001

i = 1
expect = 0
old_expect = expect
while expect - old_expect > e or i < 3:
    prev_row = PNumHouses[i]

    new_row = [0, 0, 0, 0, 0, 0, 0, 0]
    new_row[3] = prev_row[3] / TOTAL_COMB  # Has to be exactly the same
    # P(already n houses)*number of ways to chose matching*number of ways to choose non-matching
    new_row[4] = (prev_row[4] * 4 + prev_row[3] * 3 * 4) / TOTAL_COMB
    new_row[5] = (prev_row[5] * 10 + prev_row[4] * 6 * 3 + prev_row[3] * 3 * 6) / TOTAL_COMB
    new_row[6] = (prev_row[6] * 20 + prev_row[5] * 10 * 2 + prev_row[4] * 4 * 3 + prev_row[3] * 4) / TOTAL_COMB
    # Actually the probability you get your 7th house this round
    new_row[7] = (prev_row[6] * 15 + prev_row[5] * 5 + prev_row[4]) / TOTAL_COMB
    PNumHouses.append(new_row)
    i += 1

    old_expect = expect
    expect += PNumHouses[i][7] * i

print(expect)
