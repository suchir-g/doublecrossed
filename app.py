from flask import Flask, jsonify, request, render_template
from game.DotsAndBoxes import DotsAndBoxes

app = Flask(__name__)

game = None


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route('/start', methods=['POST'])
def start_game():
    global game
    data = request.get_json()
    width = data.get('width', 4) 
    height = data.get('height', 4)
    player = data.get('player', 0)
    game = DotsAndBoxes(height, width, player)
    return jsonify({'message': 'New game started', 'success': True})


@app.route('/move', methods=['POST'])
def make_move():
    global game
    if not game:
        return jsonify({'message': 'Game not started', 'successful': False}), 400

    data = request.get_json()
    line_type = data['lineType']
    vPos = data['vPos']
    hPos = data['hPos']
    player = data['player']

    successful = game.playMove(line_type, vPos, hPos, player)
    if successful:
        game_state = game.exportToString()
        return jsonify({'successful': True, 'gameState': game_state, 'message': 'Move successful'})
    else:
        return jsonify({'successful': False, 'message': 'Move failed'})


@app.route('/status', methods=['GET'])
def get_status():
    if game:
        game_state = game.exportToString()
        return jsonify({'gameState': game_state, 'successful': True})
    return jsonify({'message': 'Game not started', 'successful': False})


if __name__ == '__main__':
    app.run(debug=True)
