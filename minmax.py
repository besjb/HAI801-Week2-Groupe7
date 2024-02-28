import numpy as np
import time

def is_game_over(grid):
    return np.any(np.all(grid == 'X', axis=1)) or np.any(np.all(grid == 'X', axis=0)) or np.any(np.all(grid == 'O', axis=1)) or np.any(np.all(grid == 'O', axis=0)) or np.all(np.diag(grid) == 'X') or np.all(np.diag(np.fliplr(grid)) == 'X') or np.all(np.diag(grid) == 'O') or np.all(np.diag(np.fliplr(grid)) == 'O') or np.all(grid != '-')

def score_state(grid):
    if np.any(np.all(grid == 'X', axis=1)) or np.any(np.all(grid == 'X', axis=0)) or np.all(np.diag(grid) == 'X') or np.all(np.diag(np.fliplr(grid)) == 'X'):
        return 10
    elif np.any(np.all(grid == 'O', axis=1)) or np.any(np.all(grid == 'O', axis=0)) or np.all(np.diag(grid) == 'O') or np.all(np.diag(np.fliplr(grid)) == 'O'):
        return -10
    else:
        return 0

def minimax(grid, depth, is_maximizing):
    if is_game_over(grid):
        return score_state(grid)

    if is_maximizing:
        best_score = -np.inf
        for i in range(3):
            for j in range(3):
                if grid[i][j] == '-':
                    grid[i][j] = 'X'
                    score = minimax(grid, depth + 1, False)
                    grid[i][j] = '-'
                    best_score = max(best_score, score)
        return best_score
    else:
        best_score = np.inf
        for i in range(3):
            for j in range(3):
                if grid[i][j] == '-':
                    grid[i][j] = 'O'
                    score = minimax(grid, depth + 1, True)
                    grid[i][j] = '-'
                    best_score = min(best_score, score)
        return best_score

def best_move(grid):
    best_score = -np.inf
    best_move = None
    for i in range(3):
        for j in range(3):
            if grid[i][j] == '-':
                grid[i][j] = 'X'
                score = minimax(grid, 0, False)
                grid[i][j] = '-'
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move

def choose_empty_cell(grid):
    empty_cells = np.argwhere(grid == '-')
    return tuple(empty_cells[np.random.randint(len(empty_cells))])

def play_game(grid, symbol):
    grid = np.array(grid)  # convert grid to numpy array
    current_player = symbol
    while not is_game_over(grid):
        if current_player == 'X':
            move = best_move(grid)
        else:
            move = choose_empty_cell(grid)
        grid[move] = current_player
        current_player = 'O' if current_player == 'X' else 'X'
    return 1 if np.any(np.all(grid == 'X', axis=1)) or np.any(np.all(grid == 'X', axis=0)) or np.all(np.diag(grid) == 'X') or np.all(np.diag(np.fliplr(grid)) == 'X') else (-1 if np.any(np.all(grid == 'O', axis=1)) or np.any(np.all(grid == 'O', axis=0)) or np.all(np.diag(grid) == 'O') or np.all(np.diag(np.fliplr(grid)) == 'O') else 0)

def generate_start_grid():
    grid = np.full((3, 3), '-')
    num_moves = np.random.randint(10)
    symbols = np.random.choice(['X', 'O'])
    for _ in range(num_moves):
        row, col = np.random.randint(3), np.random.randint(3)
        if grid[row, col] == '-':
            grid[row, col] = symbols
            symbols = 'O' if symbols == 'X' else 'X'
    return grid.tolist()

def parse_grids_from_file(file_path):
    grids = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if len(line) < 10:
                line += '-' * (10 - len(line))
            symbol = line[0]
            values = line[1:]
            values = values.replace(' ', '-')
            grid = [list(values[i:i+3]) for i in range(0, len(values), 3)]
            grids.append((symbol, grid))
    return grids

if __name__ == "__main__":
    np.random.seed(int(time.time()))
    file_path = "data/dataset.txt"  # Replace "your_file.txt" with the path to your file
    grids = parse_grids_from_file(file_path)

    nb_lose = 0
    nb_win = 0
    nb_draw = 0
    nb_lines = 4519
    total_duration = 0

    for symbol, grid in grids:
        start = time.time()
        result = play_game(grid, symbol)
        end = time.time()
        total_duration += end - start

        if result == -1:
            nb_lose += 1
        elif result == 1:
            nb_win += 1
        else:
            nb_draw += 1

    print("Win rate  = {:.2f} %".format(nb_win * 100 / nb_lines))
    print("Lose rate = {:.2f} %".format(nb_lose * 100 / nb_lines))
    print("Draw rate = {:.2f} %".format(nb_draw * 100 / nb_lines))
    print("AVG duration = {:.4f} s".format(total_duration / nb_lines))
    print("Full duration = {:.4f} s".format(total_duration))
