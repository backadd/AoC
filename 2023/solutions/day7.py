"""https://adventofcode.com/2023/day/7"""

from collections import Counter
from pathlib import Path

# Constants
FIVE_OF_A_KIND = 6
FOUR_OF_A_KIND = 5
FULL_HOUSE = 4
THREE_OF_A_KIND = 3
TWO_PAIRS = 2
ONE_PAIR = 1
HIGH_CARD = 0


def getInput(test: bool = False):
    # READ INPUT
    file_path = (
        Path("./2023/inputs/7-test.txt") if test else Path("./2023/inputs/7.txt")
    )
    data = file_path.read_text().strip().split("\n")
    return data


label_dict = {
    "A": 12,
    "K": 11,
    "Q": 10,
    "T": 9,
    "9": 8,
    "8": 7,
    "7": 6,
    "6": 5,
    "5": 4,
    "4": 3,
    "3": 2,
    "2": 1,
    "J": 0,
}


class Hand:
    def __init__(self, line):
        self.hand = line.split()[0]
        self.bet = int(line.split()[1])
        self.type = self.determine_hand_type()

    def determine_hand_type(self):
        hand_without_jokers = self.hand.replace("J", "")
        number_of_jokers = self.hand.count("J")

        if number_of_jokers == 5:
            return FIVE_OF_A_KIND

        hand_counter = Counter(hand_without_jokers)
        most_common_card_count = hand_counter.most_common(1)[0][1]

        if most_common_card_count + number_of_jokers == 5:
            return FIVE_OF_A_KIND
        elif most_common_card_count + number_of_jokers == 4:
            return FOUR_OF_A_KIND
        elif (
            most_common_card_count + number_of_jokers == 3
            and hand_counter.most_common(2)[1][1] == 2
        ):
            return FULL_HOUSE
        elif most_common_card_count + number_of_jokers == 3:
            return THREE_OF_A_KIND
        elif most_common_card_count == 2 and hand_counter.most_common(2)[1][1] == 2:
            return TWO_PAIRS
        elif most_common_card_count + number_of_jokers == 2:
            return ONE_PAIR
        else:
            return HIGH_CARD


def tie_break(first_hand, second_hand):
    i = 0
    while i < len(first_hand.hand) and first_hand.hand[i] == second_hand.hand[i]:
        i += 1
    if label_dict[first_hand.hand[i]] > label_dict[second_hand.hand[i]]:
        return 1
    else:
        return 2


def sort_hands(hands: list):
    sorted_hands = []
    for hand in hands:
        if len(sorted_hands) == 0:
            sorted_hands.append(hand)
        else:
            for i in range(0, len(sorted_hands)):
                if (hand.type < sorted_hands[i].type) or (
                    hand.type == sorted_hands[i].type
                    and tie_break(hand, sorted_hands[i]) == 2
                ):
                    sorted_hands.insert(i, hand)
                    break
                elif i == len(sorted_hands) - 1:
                    sorted_hands.append(hand)
    return sorted_hands


def main():
    data = getInput()
    hands = [Hand(line) for line in data]
    sorted_hands = sort_hands(hands)
    answer = sum(hand.bet * (i + 1) for i, hand in enumerate(sorted_hands))
    print(f"Answer: {answer}")


if __name__ == "__main__":
    main()
