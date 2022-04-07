import csv
import pandas as pd
import numpy as np

# Main
if __name__ == "__main__":
    # Import popular board game csv file, add column of Solo Player that identifies as 'support solo' or 'not support solo' based on Min_Players
    df = pd.read_csv("popular_board_game.csv")
    solo = df
    solo['Solo Player'] = np.where(df['min_players'] == 1, 'support solo', 'not support solo')
    # print(solo.head(5))

    # Once we have solo, we need to create calculated columns based on groupings
    print(solo[solo['Solo Player']=='support solo'].count())
    #print(solo.pivot(index='Solo Player', columns='category', values='avg_rating'))

    # Create multi-index table for output
    outside = ['support solo', 'not support solo']
    inside = ['Best Game', 'Game Count', 'Avg Game Rating', 'Avg Game Playtime']
    hier_index = list(zip(outside, inside))
    hier_index = pd.MultiIndex.from_tuples(hier_index)
    output_df = pd.DataFrame(np.random.randn(8,5),hier_index,['Bluffing', 'Deduction', 'Economic', 'Fighting', 'Party Game'])
    print(output_df)