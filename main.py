from card import Card, CardFace, Input5Cards, Input7Cards
from player import Player, Dealer, Collector
from judge import Judge
from typing import List
import mmcv
import logging
import time


def get_logger():
    timestamp = int(time.time())
    logger = logging.getLogger('texasPoker')
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(f'log/test_{timestamp}.log')
    # ff = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # fh.setFormatter(ff)
    logger.addHandler(fh)
    return logger


def test_5_cards():
    input_5_cards = Input5Cards()
    input_5_cards.NCList[0] = Card(CardFace.SA)
    input_5_cards.NCList[1] = Card(CardFace.S2)
    input_5_cards.NCList[2] = Card(CardFace.S3)
    input_5_cards.NCList[3] = Card(CardFace.S4)
    input_5_cards.NCList[4] = Card(CardFace.S5)
    
    pattern = Judge.judge_pattern_5(input_5_cards)
    
    print(pattern.pattern_face)
    print(pattern.pattern_weight)
    

def test_7_cards():
    input_7_cards = Input7Cards()
    input_7_cards.NCList[0] = Card(CardFace.H8)
    input_7_cards.NCList[1] = Card(CardFace.CJ)
    input_7_cards.NCList[2] = Card(CardFace.SQ)
    input_7_cards.NCList[3] = Card(CardFace.D9)
    input_7_cards.NCList[4] = Card(CardFace.C7)
    input_7_cards.NCList[5] = Card(CardFace.ST)
    input_7_cards.NCList[6] = Card(CardFace.D6)
    
    keepcards, pattern = Judge.judge_pattern_7(input_7_cards)
    
    print(keepcards)
    print(pattern.pattern_face)
    print(pattern.pattern_weight)


def test_3_players():
    
    logger = get_logger()
    
    num_test = 1000
    num_players = 3
    
    deal = Dealer()
    players: List[Player] = [Player() for _ in range(num_players)]
    collectors: List[Collector] = [Collector() for _ in range(num_players)] 
    handcards = deal.deal_handcards(num_players)
    
    logger.info('='*20)
    for player, handcard in zip(players, handcards):
        player.set_handcards(handcard)
        logger.info(f'Player{player.id}: {player.handcards}')
    logger.info('='*20)
    
    for ii in mmcv.track_iter_progress(range(num_test)):

        logger.info(f'GameRound {ii}')
        sharedcards = deal.deal_sharedcards(num_times=1)[0]
        player_sharedcards = Input5Cards()
        player_sharedcards.set_cards(sharedcards)
        logger.info(player_sharedcards)
        logger.info('-'*20)
        
        pattern_list = []
        
        for player in players:
            player.set_handshare(sharedcards)
            player.get_keepcards()
            pattern_list.append(player.pattern)
            logger.info(f'Player{player.id}: {player.handshare}')
            logger.info(f'Player{player.id}: {player.keepcards}')
            logger.info(f'Player{player.id}: {player.pattern.pattern_face}')
            logger.info(f'Player{player.id}: {player.pattern.pattern_weight}')
            logger.info('-'*20)
        
        results = Judge.judge_x_players(pattern_list)
        for collector, result in zip(collectors, results):
            collector.update(result)
            logger.info(f'Player{collector.id}: {result.name}')
        
        logger.info('\n')
    
    logger.info('='*20)
    for collector in collectors:
        logger.info(f'Player{collector.id} wins: {collector.wins}')
        logger.info(f'Player{collector.id} lose: {collector.lose}')
        logger.info(f'Player{collector.id} draw: {collector.draw}')
        logger.info(f'Player{collector.id} wins_ratio: {collector.wins_str}')
        logger.info(f'Player{collector.id} lose_ratio: {collector.lose_str}')
        logger.info(f'Player{collector.id} draw_ratio: {collector.draw_str}')
        logger.info('-'*20)
    logger.info('='*20)


def test_2_shareds():
    
    logger = get_logger()
    
    num_test = 1000
    num_players = 2
    
    deal = Dealer()
    players: List[Player] = [Player() for _ in range(num_players)]
    collectors: List[Collector] = [Collector() for _ in range(num_players)] 
    handcards = [
        [Card(CardFace.SK), Card(CardFace.D8)],
        [Card(CardFace.C7), Card(CardFace.ST)]
    ]
    deal.set_show_cards(sum(handcards, []))
    
    logger.info('='*20)
    for player, handcard in zip(players, handcards):
        player.set_handcards(handcard)
        logger.info(f'Player{player.id}: {player.handcards}')
    logger.info('='*20)
    
    for ii in mmcv.track_iter_progress(range(num_test)):

        logger.info(f'GameRound {ii}')
        sharedcards = deal.deal_sharedcards(num_times=1)[0]
        player_sharedcards = Input5Cards()
        player_sharedcards.set_cards(sharedcards)
        logger.info(player_sharedcards)
        logger.info('-'*20)
        
        pattern_list = []
        
        for player in players:
            player.set_handshare(sharedcards)
            player.get_keepcards()
            pattern_list.append(player.pattern)
            logger.info(f'Player{player.id}: {player.handshare}')
            logger.info(f'Player{player.id}: {player.keepcards}')
            logger.info(f'Player{player.id}: {player.pattern.pattern_face}')
            logger.info(f'Player{player.id}: {player.pattern.pattern_weight}')
            logger.info('-'*20)
        
        results = Judge.judge_x_players(pattern_list)
        for collector, result in zip(collectors, results):
            collector.update(result)
            logger.info(f'Player{collector.id}: {result.name}')
        
        logger.info('\n')
    
    logger.info('='*20)
    for collector in collectors:
        logger.info(f'Player{collector.id} wins: {collector.wins}')
        logger.info(f'Player{collector.id} lose: {collector.lose}')
        logger.info(f'Player{collector.id} draw: {collector.draw}')
        logger.info(f'Player{collector.id} wins_ratio: {collector.wins_str}')
        logger.info(f'Player{collector.id} lose_ratio: {collector.lose_str}')
        logger.info(f'Player{collector.id} draw_ratio: {collector.draw_str}')
        logger.info('-'*20)
    logger.info('='*20)


if __name__ == '__main__':
    
    # test_7_cards()
    # test_3_players()
    test_2_shareds()