from DotsAndBoxes import DotsAndBoxes


def playGame():
    game = DotsAndBoxes(4, 4)

    def playerMove():
        game.displayGrid()
        move_valid = False
        while not move_valid:
            line_type = input(
                "Enter the line type (v for vertical, h for horizontal): ").strip()
            vPos = int(
                input("Enter the vertical position (0-indexed): ").strip())
            hPos = int(
                input("Enter the horizontal position (0-indexed): ").strip())

            if line_type in ['v', 'h']:
                if line_type == 'v' and (0 <= vPos < game.height - 1) and (0 <= hPos < game.width):
                    if game.verticalLines[vPos][hPos] == 0:
                        move_valid = True
                        box_completed = game.playMove(
                            line_type, vPos, hPos, game.playerTurn)
                    else:
                        print("Invalid move: Line already exists.")
                elif line_type == 'h' and (0 <= vPos < game.height) and (0 <= hPos < game.width - 1):
                    if game.horizontalLines[vPos][hPos] == 0:
                        move_valid = True
                        box_completed = game.playMove(
                            line_type, vPos, hPos, game.playerTurn)
                    else:
                        print("Invalid move: Line already exists.")
                else:
                    print("Invalid move: Position out of bounds.")
            else:
                print("Invalid move: Incorrect line type.")
        return box_completed

    while not game.isGameOver():
        if game.playerTurn == 0:
            box_completed = playerMove()
        else:
            print("AI's turn...")
            best_move = game.makeMove()
            if best_move:
                print(f"AI played: {best_move}")
                line_type, vPos, hPos = best_move
                box_completed = game.playMove(
                    line_type, vPos, hPos, game.playerTurn)

        game.displayGrid()
        print(
            f"Scores - Player 0: {game.boxCounts[0]}, Player 1: {game.boxCounts[1]}")

        # check if extra turn is needed
        if not box_completed:
            game.playerTurn = 1 - game.playerTurn

    print("Game over!")
    if game.boxCounts[0] > game.boxCounts[1]:
        print("Player 0 wins!")
    elif game.boxCounts[0] < game.boxCounts[1]:
        print("Player 1 wins!")
    else:
        print("It's a draw!")


playGame()