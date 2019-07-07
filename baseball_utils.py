import pandas as pd


# Function to prepare called-pitches dataframe for modelling
# Output: X, y
# X is a dataframe of observations of the input variables
# y is a series of observations of the response variable
# Function may take the better part of a minute to run
# This is almost entirely due to the line which creates the UPM column
def prepare_df(df):
    # Drop counts where number of balls is > 3
    df = df[df['count'].apply(lambda x: x[0]!='4')]
    
    # Convert strike-given-called to int
    df['strike_given_called'] = df['strike_given_called'].apply(int)
    
    # Make column to check when umpire's race matches pitcher's race
    # (1 if match, 0 if mismatch)
    df['upm'] = df.apply(lambda x: x.pitcher_race==x.umpire_race, axis=1).apply(int)
    
    # Drop the race-value columns
    df = df.drop(labels=['pitcher_race', 'umpire_race'], axis=1)
    
    # Convert innings greater than the ninth to 9
    df.inning = df.inning.apply(lambda x: min(x,9))
    
    # Turn counts and innings into dummy variables
    df = pd.get_dummies(df, columns=['count', 'inning'], drop_first=True)
    
    # Rearrange and rename columns
    new_cols = ['strike_given_called', 'upm', 'home_pitcher', 'run_diff',
            'count_0-1', 'count_0-2', 'count_1-0', 'count_1-1', 'count_1-2', 'count_2-0', 'count_2-1', 'count_2-2',
           'count_3-0', 'count_3-1', 'count_3-2',
           'inning_2', 'inning_3', 'inning_4', 'inning_5', 'inning_6', 'inning_7', 'inning_8', 'inning_9']
    df = df[new_cols]
    df = df.rename(columns={'inning_9': 'inning_9+'})
    
    # Add intercept column
    df['intercept'] = 1
    
    # Return X dataframe, y series
    return df.drop(labels=['strike_given_called'], axis=1), df['strike_given_called'] 