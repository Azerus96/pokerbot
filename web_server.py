from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO
import asyncio
from app import main  # Импорт основной логики игры (турнир и MCCFR)
from poker_game import PokerGame
from player import PokerPlayer

app = Flask(__name__)
socketio = SocketIO(app)

# Создаём объект турнира (глобальная переменная для примера)
current_game = None

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Лобби турнира
@app.route('/tournament')
def tournament():
    return render_template('tournament.html')

# Страница регистрации игрока (реальный игрок)
@app.route('/register', methods=['POST', 'GET'])
def register():
    global current_game

    if request.method == 'POST':
        player_name = request.form['player_name']
        new_player = PokerPlayer(name=player_name, stack=10000, use_mccfr=False)  # Реальный игрок
        current_game.add_player(new_player)  # Добавляем игрока к текущему турниру
        return redirect('/tournament')

    return render_template('player.html')

# Функция для отправки состояния турнира через WebSockets
def update_tournament_state(state):
    socketio.emit('update_tournament', state)

# Событие, когда реальный игрок делает действие (например, fold, call, raise)
@socketio.on('player_action')
def handle_player_action(data):
    action = data['action']
    raise_value = data.get('raise', 0)
    print(f"Player action: {action}, Raise: {raise_value}")
    # Логика выполнения действий игрока (реализуй корректно в игровой логике)
    # Например, можно использовать методы обработки действий в PokerPlayer

# Асинхронный запуск Flask
def start_flask():
    socketio.run(app, host='0.0.0.0', port=10000)

# Основной запуск турнира и веб-сервера
if __name__ == "__main__":
    # Создаём новый турнир (или загружаем)
    current_game = PokerGame(setup_tournament(num_players=160), PokerTournamentConfig())

    # Запускаем симуляцию турнира в отдельном асинхронном процессе
    asyncio.run(main())

    # Запускаем веб-сервер для взаимодействия через браузер
    start_flask()
