import pandas as pd
import numpy as np

# Tools for recursive feature selection
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import RFE

# Tools for fitting logistic regression and getting p-values
import statsmodels.api as sm

# For plotting
import matplotlib.pyplot as plt


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





### Function to rank features on significance
#       uses recursive feature selection
# Inputs:
#   X - the input variable dataframe
#   y - the response variable series
#
# Returns:
#   ranked_features - a list of column names, in decreasing order of significance
#                       omits intercept
def rank_features (X, y):
    # Fit logistic regression
    rfe = RFE(LogisticRegression(solver="liblinear"),1).fit(X, y)

    # Get ranked features
    ranked_features = [X.columns.tolist()[np.where(rfe.ranking_ == i)[0][0]] for i in range(1,len(X.columns)+1)]

    # Remove intercept
    ranked_features.remove('intercept')

    # Return list
    return ranked_features





### Function to calculate p-values and UPM coefficients for model as features are
### removed one by one in order of increasing significance
#
# Inputs:
#   X - the input variable dataframe
#   y - the response variable series
#   rf - a list of column names given in increasing significance of the features
#
# NOTE: This function anticipates UPM being included in the list of features
#
# Returns:
#   n_features, beta, p
#   n_features: a list of number-of-features corresponding to the number of features in each index of beta and p
#   beta:   a list of UPM coefficients; beta[i] is the UPM coefficient n_features[i] number of features
#   p:  a list of p-values for the UPM coefficients at the corresponding index
def eliminate_features (X, y, ranked_features):
    # Only care about the control features
    rf = ranked_features.copy()
    rf.remove('upm')

    # Initialize lists for the algorithm
    n_features = []
    beta = []
    p = []

    # While the list of control features is non-empty
    while (rf):
        # Record number of features
        n_features.append(len(rf) + 1)
        print(f"Fitting {n_features[-1]} variables...")

        # Fit logistic regression
        fit = sm.Logit(y, X[['upm', 'intercept'] + rf]).fit()

        # Record coefficient and p-value
        beta.append(fit.params[0])
        p.append(fit.pvalues[0])
        print(f"Beta = {beta[-1]}; p = {p[-1]}")

        # Remove least significant control from list
        rf = rf[:-1]

    return n_features, beta, p




### Functions to make plotting betas and p-values shorted in notebook
### Inputs:
# beta or p: list of coefficients or p-values output by eliminate_features()
# n_features: n_features output by eliminate_features()
# title: Plot title
# outfile: Name of output file to write plot to. File extension given determines format,
#           since matplotlib.pyplot.savefig() is used.

def plot_beta(beta, n_features, title, outfile):
    plt.figure(figsize=(9,7))
    plt.ylim(min(min(beta), 0), max(0,max(beta)))
    plt.plot(n_features, beta)
    plt.xlabel("Number of features")
    plt.ylabel("UPM Coefficient")
    plt.xticks(n_features)
    plt.title(title)
    plt.savefig(outfile)
    plt.show()


def plot_pvalues (p, n_features, title, outfile):
    plt.figure(figsize=(9,7))
    plt.ylim(0,1)
    plt.plot(n_features, p)

    plt.xlabel("Number of features")
    plt.ylabel("UPM p-value")
    plt.title(title)
    plt.xticks(n_features)
    plt.savefig(outfile)


# Function to find ∂y/∂x_upm for x_upm = 0, x_i = mean(x_i) for all i ≠ upm
# Purpose is to describe the effect of the UPM coefficient in the logistic regression model
# The formula in use below can be easily derived by taking the partial derivative of the sigmoid function
#
# Inputs:
#   fit - a logistic regression fit by statsmodels.api.Logit(y, X).fit()
#   X - the X dataframe of input variables used to make the corresponding fit
#
# Returns: the partial derivative of the sigmoid function with respect to the UPM indicator variable
#   evaluated at x_UPM = 0, all other inputs set to their mean
def upm_effects(fit, X):
    # Find predicted value
    pred = fit.predict([0] + X.mean()[1:].tolist())[0]
    
    return (fit.params[0]*(pred - pred**2))





# Simple function for passing, to group racial categories into a binary:
# White, or nonwhite
def white_or_not(r):
    if r == 'white':
        return 'white'
    else:
        return 'nonwhite'