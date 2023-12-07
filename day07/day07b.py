"""
--- Part Two ---

To make things a little more interesting, the Elf introduces one additional rule. Now, J cards are jokers - 
wildcards that can act like whatever card would make the hand the strongest type possible.

To balance this, J cards are now the weakest individual cards, weaker even than 2. The other cards stay in the 
same order: A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J.

J cards can pretend to be whatever card is best for the purpose of determining hand type; for example, QJJQ2 is 
now considered four of a kind. However, for the purpose of breaking ties between two hands of the same type, J is 
always treated as J, not the card it's pretending to be: JKKK2 is weaker than QQQQ2 because J is weaker than Q.

Now, the above example goes very differently:
    32T3K 765
    T55J5 684
    KK677 28
    KTJJT 220
    QQQJA 483
 - 32T3K is still the only one pair; it doesn't contain any jokers, so its strength doesn't increase.
 - KK677 is now the only two pair, making it the second-weakest hand.
 - T55J5, KTJJT, and QQQJA are now all four of a kind! T55J5 gets rank 3, QQQJA gets rank 4, and KTJJT 
   gets rank 5.
With the new joker rule, the total winnings in this example are 5905.

Using the new joker rule, find the rank of every hand in your set. What are the new total winnings?

"""

from typing import List


class Hand:
    def __init__(self, hand: str, bid: str):
        card_vals = {
            "J": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, 
            "8": 8, "9": 9, "T": 10, "Q": 11, "K": 12, "A": 13,
        }          
        self.bid = int(bid)
        self.hand = [card_vals[c] for c in hand]
        individuals = set(self.hand)
        unique = len(individuals) - (1 in individuals) if len(individuals) > 1 else len(individuals)
        individuals.discard(1)
        counts = [self.hand.count(x) + self.hand.count(1) for x in individuals]
        self.type = min(7, abs(6 - unique) + (max(counts) >= 3) + (max(counts) >= 4)) if counts else 7

    
    def get_val(self, multiplier: int) -> int:
        return multiplier * self.bid
    
    def __lt__(self, other: [Hand]) -> bool:
        if self.type == other.type:
            return self.hand < other.hand
        return self.type < other.type


def get_total(hands: List[Hand]) -> int:
    return sum(h.get_val(i) for i, h in enumerate(sorted(hands), 1))
    
with open("data.txt") as f:
    print(get_total(sorted(Hand(*hand.split()) for hand in f.read().strip().split("\n"))))

#sum total is 251135960
