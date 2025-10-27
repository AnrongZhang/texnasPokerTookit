from card import Card, NumCards, HandCards, Input5Cards, Input7Cards
from pattern import Pattern, PatternFace
from collections import defaultdict, Counter
from typing import List
from enum import Enum


NSYS = 100


class OutCome(Enum):
    WINS = 1
    LOSE = 2
    DRAW = 3

class Judge:
    @staticmethod
    def judge_pattern_7(input: Input7Cards):
        keepcards: Input5Cards = Input5Cards()
        input.get_suits_and_weights()
        suits = input.suits
        weights = input.weights
        hasF, hasS, hasSF, suits_FS, weights_FS = Judge.hasStraightFlush(suits.copy(), weights.copy())
        if hasSF:
            cards_list = NumCards.merge_suits_and_weights(suits_FS, weights_FS)
            keepcards.set_cards(cards_list)
            pattern = Pattern(PatternFace.SRIFL, Judge.getPWeightMax(weights_FS))
            return keepcards, pattern
        hasFK, suits_FK, weights_FK = Judge.hasFK(suits.copy(), weights.copy())
        if hasFK:
            cards_list = NumCards.merge_suits_and_weights(suits_FK, weights_FK)
            keepcards.set_cards(cards_list)
            pattern = Pattern(PatternFace.FOURK, Judge.getPWeightFKFH(weights_FK))
            return keepcards, pattern
        hasFH, hasCS, suits_TH, weights_TH = Judge.hasFHCS(suits.copy(), weights.copy())
        if hasFH:
            cards_list = NumCards.merge_suits_and_weights(suits_TH, weights_TH)
            keepcards.set_cards(cards_list)
            pattern = Pattern(PatternFace.FULLH, Judge.getPWeightFKFH(weights_TH))
            return keepcards, pattern
        if hasF:
            cards_list = NumCards.merge_suits_and_weights(suits_FS, weights_FS)
            keepcards.set_cards(cards_list)
            pattern = Pattern(PatternFace.FLUSH, Judge.getPWeightAll(weights_FS))
            return keepcards, pattern
        if hasS:
            cards_list = NumCards.merge_suits_and_weights(suits_FS, weights_FS)
            keepcards.set_cards(cards_list)
            pattern = Pattern(PatternFace.STRAI, Judge.getPWeightMax(weights_FS))
            return keepcards, pattern
        if hasCS:
            cards_list = NumCards.merge_suits_and_weights(suits_TH, weights_TH)
            keepcards.set_cards(cards_list)
            pattern = Pattern(PatternFace.THREE, Judge.getPWeightTHREE(weights_TH))
            return keepcards, pattern        
        hasTP, hasOP, suits_TO, weights_TO = Judge.hasPair(suits.copy(), weights.copy())
        if hasTP:
            cards_list = NumCards.merge_suits_and_weights(suits_TO, weights_TO)
            keepcards.set_cards(cards_list)
            pattern = Pattern(PatternFace.TPAIR, Judge.getPWeightTPAIR(weights_TO))
            return keepcards, pattern
        if hasOP:
            cards_list = NumCards.merge_suits_and_weights(suits_TO, weights_TO)
            keepcards.set_cards(cards_list)
            pattern = Pattern(PatternFace.OPAIR, Judge.getPWeghtOPAIR(weights_TO))
            return keepcards, pattern
        suits_AH, weights_AH = Judge.getAHigh(suits.copy(), weights.copy())
        cards_list = NumCards.merge_suits_and_weights(suits_AH, weights_AH)
        keepcards.set_cards(cards_list)
        pattern = Pattern(PatternFace.AHIGH, Judge.getPWeightAll(weights_AH))
        return keepcards, pattern
    
    @staticmethod
    def judge_pattern_5(input: Input5Cards):
        input.get_suits_and_weights()
        suits = input.suits
        weights = input.weights
        isS, isF = Judge.isStraightFlush(suits, weights)
        if isS and isF:
            return Pattern(PatternFace.SRIFL, Judge.getPWeightMax(weights))
        isFK, isFH = Judge.isFKFH(weights)
        if isFK:
            return Pattern(PatternFace.FOURK, Judge.getPWeightFKFH(weights))
        if isFH:
            return Pattern(PatternFace.FULLH, Judge.getPWeightFKFH(weights))
        if isF:
            return Pattern(PatternFace.FLUSH, Judge.getPWeightAll(weights))
        if isS:
            return Pattern(PatternFace.STRAI, Judge.getPWeightMax(weights))
        isCS, isTP = Judge.isCSTP(weights)
        if isCS:
            return Pattern(PatternFace.THREE, Judge.getPWeightTHREE(weights))
        if isTP:
            return Pattern(PatternFace.TPAIR, Judge.getPWeightTPAIR(weights))
        isOP = Judge.isOnePair(weights)
        if isOP:
            return Pattern(PatternFace.OPAIR, Judge.getPWeghtOPAIR(weights))
        return Pattern(PatternFace.AHIGH, Judge.getPWeightAll(weights))
    
    @staticmethod
    def hasFlush(suits, weights):
        hasF = False
        suits_left = []
        weights_left = []
        counter = Counter(suits)
        count_0 = counter.most_common(1)[0]
        if count_0[1] >= 5:
            hasF = True
            for suit, weight in zip(suits, weights):
                if suit == count_0[0]:
                    weights_left.append(weight)
                    suits_left.append(suit)
            weights_left.sort(reverse=True)
        return hasF, suits_left, weights_left
    
    @staticmethod
    def hasStraight(weights):
        hasS = False
        weights_list = [weights]
        if 14 in weights:
            weights_list.append([1 if weight == 14 else weight for weight in weights])
        for weights in weights_list:
            weights_left = []
            weights.sort()
            for ii in range(len(weights) - 1):
                dd = weights[ii+1] - weights[ii]
                if dd == 0:
                    continue
                if dd == 1:
                    if len((weights_left)) == 0:
                        weights_left.append(weights[ii])
                    weights_left.append(weights[ii+1])
                else:
                    if len(weights_left) >= 5:
                        break
                    weights_left = []
            if len(weights_left) >= 5:
                hasS = True
                break
        return hasS, weights_left
    
    @staticmethod
    def hasStraightFlush(suits, weights):
        hasSF = False
        hasF, suits_f, weights_f = Judge.hasFlush(suits, weights)
        if hasF:
            hasS, weights_sf = Judge.hasStraight(weights_f)
            if hasS:
                hasSF = True
                suits = suits_f[:5]
                weights = weights_sf[-5:]
            else:
                suits = suits_f[:5]
                weights = weights_f[:5]
        else:
            hasS, weights_s = Judge.hasStraight(weights)
            if hasS:
                sw_dict = defaultdict(list)
                for suit, weight in zip(suits, weights):
                    sw_dict[weight].append(suit)
                    if 1 in weights_s and weight == 14:
                        sw_dict[1].append(suit)
                weights = weights_s[-5:]
                suits = []
                for weight in weights:
                    suits.append(sw_dict[weight][0])
            else:
                suits = []
                weights = []
        return hasF, hasS, hasSF, suits, weights
    
    @staticmethod
    def hasFK(suits, weights):
        counter = Counter(weights)
        counter_0 = counter.most_common(1)[0]
        if counter_0[1] != 4:
            return False, [], []
        weight_4 = counter_0[0]
        suit_max = None; weight_max = 0
        for suit, weight in zip(suits, weights):
            if weight == weight_4:
                continue
            if weight > weight_max:
                weight_max = weight
                suit_max = suit
        
        suits_left = [1, 2, 3, 4, suit_max]
        weights_left = [weight_4 for _ in range(4)] + [weight_max]
        return True, suits_left, weights_left
    
    @staticmethod
    def hasFHCS(suits, weights):
        has_FH = False
        has_CS = False
        counter = Counter(weights)
        counter_0, counter_1 = counter.most_common(2)
        if counter_0[1] != 3:
            return False, False, [], []
        if counter_1[1] == 3:
            has_FH = True
            weight_3 = max(counter_0[0], counter_1[0])
        else:
            weight_3 = counter_0[0]
            if counter_1[1] == 2:
                has_FH = True
            else:
                has_FH = False
                has_CS = True

        suits_left = []
        weights_left = []
        suits_keep = []
        weights_keep = []
        for suit, weight in zip(suits, weights):
            if weight == weight_3:
                suits_keep.append(suit)
                weights_keep.append(weight)
            else:
                suits_left.append(suit)
                weights_left.append(weight)
        if has_FH:
            counter = Counter(weights_left)
            weight_max = 0
            for weight_, count_ in counter.items():
                if count_ >= 2:
                    weight_max = max(weight_max, weight_)
            for suit, weight in zip(suits_left, weights_left):
                if weight == weight_max:
                    weights_keep.append(weight)
                    suits_keep.append(suit)
                if len(weights_keep) >= 5:
                    break
        else:
            weights_sort = sorted(weights_left, reverse=True)
            for ii in range(2):
                weights_keep.append(weights_sort[ii])
                suits_keep.append(suits_left[weights_left.index(weights_sort[ii])])
        
        return has_FH, has_CS, suits_keep, weights_keep
        
    @staticmethod
    def hasPair(suits, weights: list):
        has_TP = False
        has_OP = False
        counter = Counter(weights)
        counter_0, counter_1, counter_2 = counter.most_common(3)
        if counter_0[1] != 2:
            return False, False, [], []
        if counter_1[1] != 2:
            has_OP = True
            weight_2 = counter_0[0]
            weights_left = []
            suits_left = []
            weights_keep = []
            suits_keep = []
            for suit, weight in zip(suits, weights):
                if weight == weight_2:
                    suits_keep.append(suit)
                    weights_keep.append(weight)
                else:
                    suits_left.append(suit)
                    weights_left.append(weight)
            weights_sort = sorted(weights_left, reverse=True)
            for ii in range(3):
                weights_keep.append(weights_sort[ii])
                suits_keep.append(suits_left[weights_left.index(weights_sort[ii])])
            return False, has_OP, suits_keep, weights_keep
        
        has_TP = True
        weight_2_list = [counter_0[0], counter_1[0]]
        if counter_2[1] == 2:
            weight_2_list.append(counter_2[0])
        weight_2_list.sort(reverse=True)
        weight_2_list = weight_2_list[:2]
        weight_max = 0
        suits_keep = []
        weights_keep = []
        for suit, weight in zip(suits, weights):
            if weight in weight_2_list:
                suits_keep.append(suit)
                weights_keep.append(weight)
            else:
                weight_max = max(weight_max, weight)
        
        weights_keep.append(weight_max)
        suits_keep.append(suits[weights.index(weight_max)])
        return has_TP, False, suits_keep, weights_keep
            
    @staticmethod
    def getAHigh(suits, weights: list):
        weights_keep = []
        suits_keep = []
        weights_sort = sorted(weights, reverse=True)
        for ii in range(5):
            weights_keep.append(weights_sort[ii])
            suits_keep.append(suits[weights.index(weights_sort[ii])])
        return suits_keep, weights_keep
                    
    @staticmethod
    def isFlush(suits):
        return len(Counter(suits)) == 1
            
    @staticmethod
    def isStraight(weights):
        weights_list = [weights]
        if 14 in weights:
            weights_list.append([1 if weight == 14 else weight for weight in weights])
        for weights in weights_list:
            weights.sort()
            dis = [weights[i+1] - weights[i] for i in range(4)]
            counter = Counter(dis)
            if len(counter) == 1 and counter.get(1) == 4:
                return True
        return False
        
    @staticmethod
    def isFKFH(weights):
        isFK = False
        isFH = False
        counter = Counter(weights)
        if len(counter) == 2:
            if counter.most_common(1)[1] == 3:
                isFH = True
            else:
                isFK = True
        return isFK, isFH
    
    @staticmethod
    def isCSTP(weights):
        isCS = False
        isTP = False
        counter = Counter(weights)
        if len(counter) == 3:
            if counter.most_common(1)[1] == 2:
                isTP = True
            else:
                isCS = True
        return isTP, isCS

    @staticmethod
    def isOnePair(weights):
        counter = Counter(weights)
        return len(counter) == 4
        
    @staticmethod
    def isStraightFlush(suits, weights):
        isF = Judge.isFlush(suits)
        isS = Judge.isStraight(weights)
        return isS, isF
        
    @staticmethod
    def getPWeightMax(weights):
        if 14 not in weights:
            return max(weights)
        if 13 in weights:
            return 14
        return 5
    
    @staticmethod
    def getPWeightFKFH(weights):
        counter = Counter(weights)
        most_common = counter.most_common(2)
        weights_all = most_common[0][0] * NSYS + most_common[1][0]
        return weights_all
    
    @staticmethod
    def getPWeightTHREE(weights):
        counter = Counter(weights)
        most_common = counter.most_common(3)
        weights_all = most_common[0][0] * (NSYS ** 2)
        weights_all += max(most_common[1][0], most_common[2][0]) * NSYS
        weights_all += min(most_common[1][0], most_common[2][0])
        return weights_all
        
    @staticmethod
    def getPWeightTPAIR(weights):
        counter = Counter(weights)
        most_common = counter.most_common(3)
        weights_all = most_common[2][0]
        weights_all += max(most_common[0][0], most_common[1][0]) * (NSYS ** 2)
        weights_all += min(most_common[0][0], most_common[1][0]) * NSYS
        return weights_all
    
    @staticmethod
    def getPWeghtOPAIR(weights):
        counter = Counter(weights)
        pair_num = counter.most_common(1)[0][0]
        weights = list(counter.keys())
        weights.remove(pair_num)
        weight_all = pair_num * (NSYS ** 3)
        weights.sort(reverse=False)
        for ii in range(3):
            weight_all += weights[ii] * (NSYS ** ii)
        return weight_all        
    
    @staticmethod
    def getPWeightAll(weights: list):
        weights.sort()
        weight_all = 0
        for ii in range(5):
            weight_all += weights[ii] * (NSYS ** ii) 
        return weight_all
    
    @staticmethod
    def judge_2_players(pattern_1: Pattern, pattern_2: Pattern):
        if pattern_1.pattern_face.value > pattern_2.pattern_face.value:
            return OutCome.WINS
        elif pattern_1.pattern_face.value < pattern_2.pattern_face.value:
            return OutCome.LOSE
        elif pattern_1.pattern_weight > pattern_2.pattern_weight:
            return OutCome.WINS
        elif pattern_1.pattern_weight < pattern_2.pattern_weight:
            return OutCome.LOSE
        else:
            return OutCome.DRAW
        
    @staticmethod
    def judge_x_players(pattern_list: List[Pattern]):
        scores = [0 for _ in range(len(pattern_list))]
        scores[0] = 1
        max_score = 1
        max_pattern = pattern_list[0]
        for ii in range(1, len(pattern_list)):
            result = Judge.judge_2_players(pattern_list[ii], max_pattern)
            if result == OutCome.DRAW:
                scores[ii] = max_score
            if result == OutCome.WINS:
                max_score += 1
                scores[ii] = max_score
                max_pattern = pattern_list[ii]
        counter = Counter(scores)
        results = []
        for score in scores:
            if score < max_score:
                results.append(OutCome.LOSE)
            elif counter[max_score] == 1:
                results.append(OutCome.WINS)
            else:
                results.append(OutCome.DRAW)
        return results
        