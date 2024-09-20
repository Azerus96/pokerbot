import os
import asyncio
from config import PokerTournamentConfig
from player import PokerPlayer
from poker_game import PokerGame
from logging_system import Logger
from database import TournamentDatabase
from utils import generate_player_name
from web_server import update_tournament_state  # Добавляем для обновления через WebSocket

# Настройки турнира
def setup_tournament(num_players=160, load_previous_state=False):
    config = PokerTournamentConfig()
    
    players = []
    for i in range(num_players):
        player_name = generate_player_name()
        player = PokerPlayer(player_name, config.starting_stack)
        
        if load_previous_state and os.path.exists(f"{player_name}_state.pkl"):
            player.load_state(f"{player_name}_state.pkl")
        players.append(player)
        
    return PokerGame(players, config)

async def main():
    num_players = 160
    logger = Logger()
    db = TournamentDatabase()  # База данных для турнира
    
    load_previous_state = False
    game = setup_tournament(num_players, load_previous_state)

    logger.log_event("Tournament started")

    try:
        await game.simulate_tournament()  # Запуск турнира

        # Логирование и сохранение результатов
        for player in game.players:
            logger.log_event(f"{player.name} закончил игровой стек с {player.stack}")
            player.save_state()
            
        logger.log_event("Tournament finished")

    except Exception as e:
        logger.log_event(f"An error occurred: {str(e)}")
