import datetime

import numpy as np
import pandas as pd
import datetime


def output_file(boards, moves, players, winner, turn_counter):
    boards = boards.reshape(225, 225)
    players = players.reshape(225, 1)
    df = pd.DataFrame(boards)
    df['x'] = moves[0]
    df['y'] = moves[1]
    df['player'] = players
    df['winner'] = np.repeat(winner, 225)
    df.iloc[:turn_counter, :].to_csv("game_logs/game_" + str(datetime.datetime.now()).replace(":", "").replace("-", "").replace(".", "").replace(" ", "") + ".csv")
