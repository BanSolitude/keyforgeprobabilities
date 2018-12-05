TOTAL_COMB = 35.0

PNumHouses = [[0, 0, 0, 0], [0, 0, 0, 1]]

e = .0000001

i = 1
expect = 0
old_expect = expect
while expect - old_expect > e or i < 3:
    prev_row = PNumHouses[i]

    new_row = [0, 0, 0, 0]
    # P(already n houses)*number of ways to chose matching*number of ways to choose non-matching
    new_row[3] = prev_row[3] / TOTAL_COMB  # Has to be exactly the same
    new_row[2] = (prev_row[3] * 3 * 4 + prev_row[2] * 5) / TOTAL_COMB
    new_row[1] = (prev_row[3] * 3 * 6 + prev_row[2] * 2 * 10 + prev_row[1] * 15) / TOTAL_COMB
    new_row[0] = (prev_row[3] * 4 + prev_row[2] * 10 + prev_row[
        1] * 20) / TOTAL_COMB  # Actually the probability you get your 7th house this round
    PNumHouses.append(new_row)
    i += 1

    old_expect = expect
    expect += PNumHouses[i][0] * i

print(expect)
