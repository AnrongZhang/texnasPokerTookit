from enum import Enum


class CardFace(Enum):
    # 黑桃
    SA = 114
    SK = 113
    SQ = 112
    SJ = 111
    ST = 110
    S9 = 109
    S8 = 108
    S7 = 107
    S6 = 106
    S5 = 105
    S4 = 104
    S3 = 103
    S2 = 102
    # 红心
    HA = 214
    HK = 213
    HQ = 212
    HJ = 211
    HT = 210
    H9 = 209
    H8 = 208
    H7 = 207
    H6 = 206
    H5 = 205
    H4 = 204
    H3 = 203
    H2 = 202
    # 方片
    DA = 314
    DK = 313
    DQ = 312
    DJ = 311
    DT = 310
    D9 = 309
    D8 = 308
    D7 = 307
    D6 = 306
    D5 = 305
    D4 = 304
    D3 = 303
    D2 = 302
    # 草花
    CA = 414
    CK = 413
    CQ = 412
    CJ = 411
    CT = 410
    C9 = 409
    C8 = 408
    C7 = 407
    C6 = 406
    C5 = 405
    C4 = 404
    C3 = 403
    C2 = 402
    # 随机牌
    R0 = 500
    # 占位牌
    P0 = 600


class Card:
    def __init__(self, card: CardFace):
        self.card = card
        
    def set_card(self, card):
        self.card = card
    
    @property
    def suit(self):
        return self.card.value // 100
    
    @property
    def weight(self):
        return self.card.value % 100
    
    def is_valid(self):
        return self.card.value < 500
    
    @property
    def name(self):
        if self.card.value == 500 or self.card.value == 600:
            return 'x'

        if self.suit == 1:
            name = r'\u2660'
        elif self.suit == 2:
            name = r'\u2764'
        elif self.suit == 3:
            name = r'\u2666'
        elif self.suit == 4:
            name = r'\u2663'
            
        if self.weight < 10:
            name += str(self.weight)
        elif self.weight == 10:
            name += 'T'
        elif self.weight == 11:
            name += 'J'
        elif self.weight == 12:
            name += 'Q'
        elif self.weight == 13:
            name += 'K'
        elif self.weight == 14:
            name += 'A'

        name = name.encode('latin-1').decode('unicode_escape')
        return name
    

class NumCards:
    def __init__(self, num_cards: int):
        self.NCList = [Card(CardFace.P0) for _ in range(num_cards)]
        
    def get_suits_and_weights(self):
        self.suits = [card.suit for card in self.NCList]
        self.weights = [card.weight for card in self.NCList]
    
    @staticmethod
    def merge_suits_and_weights(suits, weights):
        assert len(suits) == len(weights)
        cards_list = []
        for suit, weight in zip(suits, weights):
            if weight == 1:
                weight = 14
            card = Card(CardFace(value=suit * 100 + weight))
            cards_list.append(card)
        return cards_list
        
    def set_cards(self, cards_list):
        assert len(cards_list) == len(self.NCList)
        self.NCList = cards_list
    
    def __str__(self):
        p_list = []
        for card in self.NCList:
            p_list.append(card.name)
        return ' '.join(p_list)
            

class HandCards(NumCards):
    def __init__(self):
        super().__init__(2)
    
class Input7Cards(NumCards):
    def __init__(self):
        super().__init__(7)
    
class Input5Cards(NumCards):
    def __init__(self):
        super().__init__(5)
                