from card import Card, CardFace, HandCards, Input5Cards, Input7Cards
from pattern import Pattern
from judge import Judge, OutCome
from typing import List, Union
import random


class Player:
    ID = 1
    def __init__(self):
        self.handcards: HandCards = HandCards()
        self.handshare: Input7Cards = Input7Cards()
        self.keepcards: Input5Cards = None
        self.pattern: Pattern = None
        self.id = Player.ID
        Player.ID += 1
        
    def set_handcards(self, cards_list: List[Card]):
        self.handcards.set_cards(cards_list)
    
    def set_handshare(self, cards_list: List[Card]):
        self.handshare.set_cards(self.handcards.NCList + cards_list)
    
    def get_keepcards(self):
        keepcards, pattern = Judge.judge_pattern_7(self.handshare)
        self.keepcards = keepcards
        self.pattern = pattern
        

class Dealer:
    CARDS_POOL = [
        102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114,
        202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214,
        302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314,
        402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414,
    ]
    
    def __init__(self):
        self.cards_pool = Dealer.CARDS_POOL.copy()
    
    def set_show_cards(self, card_values: List[Union[Card, CardFace, int]]):
        for card_value in card_values:
            if isinstance(card_value, int):
                self.cards_pool.remove(card_value)
            elif isinstance(card_value, CardFace):
                self.cards_pool.remove(card_value.value)
            else:
                self.cards_pool.remove(card_value.card.value)
    
    def deal_handcards(self, num_players=2, x_dup=True):
        num_cards = num_players * 2
        random_numbers = random.sample(range(len(self.cards_pool)), num_cards)
        deal_results = []
        for ii in range(num_players):
            deal_results.append([
                Card(CardFace(self.cards_pool[random_numbers[ii]])),
                Card(CardFace(self.cards_pool[random_numbers[num_players + ii]]))
            ])
        if x_dup:
            self.set_show_cards(sum(deal_results, []))
        return deal_results
    
    def deal_sharedcards(self, num_times=1, x_dup=False):
        num_cards = num_times * 5
        random_numbers = random.sample(range(len(self.cards_pool)), num_cards)
        deal_results = []
        for ii in range(num_times):
            deal_result = []
            for random_num in random_numbers[ii * 5: (ii+1) * 5]:
                deal_result.append(Card(CardFace(self.cards_pool[random_num])))
            deal_results.append(deal_result)
        if x_dup:
            self.set_show_cards(deal_results)
        return deal_results
    

class Collector:
    ID = 1
    
    def __init__(self):
        self.wins: bool = 0
        self.lose: bool = 0
        self.draw: bool = 0
        self.id = Collector.ID
        Collector.ID += 1
    
    def update(self, outcome: OutCome):
        if outcome == OutCome.WINS:
            self.wins += 1
        if outcome == OutCome.LOSE:
            self.lose += 1
        if outcome == OutCome.DRAW:
            self.draw += 1
    
    @property
    def total(self):
        return self.wins + self.lose + self.draw
    
    @property
    def wins_ratio(self):
        return self.wins * 100 / self.total
    
    @property
    def lose_ratio(self):
        return self.lose * 100 / self.total
    
    @property
    def draw_ratio(self):
        return self.draw * 100 / self.total
    
    @property
    def wins_str(self):
        return f'{self.wins_ratio:.2f}%'
    
    @property
    def lose_str(self):
        return f'{self.lose_ratio:.2f}%'

    @property
    def draw_str(self):
        return f'{self.draw_ratio:.2f}%'
    