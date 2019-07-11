# Call 'Em as They See 'Em: Examining Potential Umpire Bias in Major League Baseball
### Marshall Doig, Stephanie Engeling, Willy Goal, Robert McAlmon, Ashley McGee

Our inpsiration for this project came from a review of [research done by Christopher A. Parsons, Johan Sulaeman, Michael C. Yates, and Daniel S. Hamermesh](https://www.nber.org/papers/w13665.pdf) on potential racial bias exhibited by umpires in Major League Baseball in the 2004 to 2006 seasons. In short, their research stated that when the race of the umpire matched the race of the starting pitcher, the umpire was more likely to call a strike. Additionally, they found this particular effect was only seen when there was "little scrutiny of umpires' behavior" -- that is, for example, in stadiums where there was no computerized system monitoring calls. In 2004-2006, such systems were installed in just 11 of 30 MLB stadiums, which accounted for approximately 35 percent of games played in those seasons.

## Hypothesis

Based on a granular study of the subjective racial identity of umpires and pitchers in Major League Baseball during the 2013 to 2015 seasons, we decided to examine umpires' potential bias in an attempt to corroborate or oppose the findings of Parsons et al. Our hypothesis states:

There will be a positive difference in the number of strikes called when the race of the home plate umpire matches the race of the pitcher.

Null: There will be not be any difference in the number of strikes called when the race of the home plate umpire matches the race of the pitcher.

## Data Retrieval and Cleaning

We scraped every pitch of every game of the 2013, 2014, and 2015 MLB seasons from [Baseball-Reference.com](https://www.baseball-reference.com).

![Partial play-by-play table of a game on Baseball-Reference.com](https://github.com/AshleyMcGee/MLB/blob/master/images/game_scrape_play-by-play.PNG)
*Partial play-by-play table. We turned this...*

We created code to retrieve from each game, based on the structure of each game's Play by Play table:
* Home plate umpire name
* Pitch sequence
* Pitcher name for each plate appearance
* Batter name for each plate appearance
* Inning of each plate appearance
* Score of the game during each plate appearance

![Partial dataframe of scraped game during data cleaning](https://github.com/AshleyMcGee/MLB/blob/master/images/game_scrape_dataframe.PNG)
*...into this (during cleaning process)...*

Once we scraped this data from Baseball-Reference, we transformed it to:
* Show the count of balls and strikes before each pitch
* Have only one row for each pitch
* Drop rows whose pitches were not solely dependent on the home plate umpire's discretion -- that is, we kept only rows with called strikes and called balls (not intentional balls, pitchouts, etc.). These rows corresponded with pitch code C (called strike) or B (called ball).

With each relevant pitch on its own row, we then added the race of each pitcher and umpire included in the 2013-15 game data. We compiled this data by starting with an Excel file of an MLB "player census" done by [BestTickets.com](www.besttickets.com/blog/mlb-players-census/). This Excel file only included players on each team's Opening Day roster for the 2014 season, so we then manually identified any pitchers not in the initial player census using a Google Image Search. Fortunately, the BestTickets file classified players into four groups: white, black, Hispanic, or Asian. These groups matched those used in the Parsons et al. study. For umpires, we again used a Google Image Search to determine each umpire's race (sorted into the same four categories as players). For pitchers and umpires whose race was not immediately obvious to the initial evaluator after a search, other group members were asked to provide a second opinion. Batter data helped separate each plate appearance (and therefore helped determine the ball-strike count for each pitch), but it was dropped once it was no longer needed.

When we finally had race data for all pitchers and umpires, we merged it with the game data. From there, we were able to convert the data into dummy variables that were classified into the following columns:
* `strike_given_called`: Whether the pitch was called a strike
* `upm`: Whether the umpire and pitcher race matched for that pitch
* `home_pitcher`: Whether the pitcher was pitching for the home team
* `run_diff`: The run difference for the pitcher's team at that point in the game; for example, if the pitcher's team led by 5 runs, this was 5, and if the team trailed by 4 runs, this was -4. If the game was tied, this was 0.
* `count_b-s`: Where `b` is the number of balls in the count and `s` is the number of strikes in the count.
* `inning_i`: Where `i` is the inning in which the pitch was thrown. If a pitch was thrown in extra innings, it was placed in the `inning_9` column.

At this point, the data was ready to be tested in models.

![Partial dataframe of dummy variables after data cleaning completed](https://github.com/AshleyMcGee/MLB/blob/master/images/game_scrape_dummy-variables.PNG)
*...and finally, into this.*

## Data Exploration

#### Count of total balls and strikes called

![Count of total balls and strikes called](https://github.com/AshleyMcGee/MLB/blob/master/images/strike_count.png)

* The ratio of ball vs. strike calls is **67:33**.

#### Count of pitches by pitcher race

![Count of pitches by pitcher race](https://github.com/AshleyMcGee/MLB/blob/master/images/pitcher_race_count.png)

#### Count of pitches by umpire race

![Count of pitches by umpire race](https://github.com/AshleyMcGee/MLB/blob/master/images/umpire_race_count.png)

#### Count of pitches where the umpire and pitcher are the same race

![Count of pitches where the umpire and pitcher are the same race](https://github.com/AshleyMcGee/MLB/blob/master/images/ump_count.png)

* The umpire and pitcher are more likely to be the same race than not.
* There are significantly fewer non-white pitchers and umpires than white ones.
* There are a handful of Asian pitchers but no Asian umpires.

#### Mean grouped by call

![Mean grouped by call](https://github.com/AshleyMcGee/MLB/blob/master/images/mean_groupby_call.png)

* The percentage of pitches thrown by the home team that are called strikes is higher than that of pitches thrown by the away team. Pitchers playing at home receive more strike calls.
* The average run difference of pitches called strikes is higher than that of pitches called balls. Pitches called strikes are more likely to be thrown by the team in the lead.

#### Mean grouped by the umpire and pitcher of the same race

![Mean grouped by the umpire and pitcher of the same race](https://github.com/AshleyMcGee/MLB/blob/master/images/mean_groupby_upm.png)

* The percentage of strike calls is slightly higher when the umpire and pitcher are the same race.
* Home pitchers are slightly more likely to have an umpire of a different race.
* The average run difference of pitches called by an umpire of the same race is higher than that of pitches called by an umpire of a different race. On average, the team whose current pitcher is the same race as the umpire is more likely to be in the lead.

#### Mean grouped by the pitch thrown by a pitcher at home

![Mean grouped by the pitch thrown by a pitcher at home](https://github.com/AshleyMcGee/MLB/blob/master/images/mean_groupby_home.png)

* Home pitchers are more likely to receive strike calls.
* Home pitchers are more likely to be on the team not in the lead. This is possibly due to the fact that the home team always pitches in the top of the inning, including to start the game; the away team could have more plate appearances than the home team.

#### Race vs. strike calls

![Race vs. strike calls](https://github.com/AshleyMcGee/MLB/blob/master/images/proportion_calls.png)

* Whether the umpire and pitcher are the same race does not seem like a strong predictor for called strikes based on the visualization.

## Analysis

We applied a logistic regression model to evaluate the potential effects of umpire and pitcher race on whether an umpire would be more likely to call a ball or a strike.

After some testing with the model, we found that the significance of `upm` (umpire-pitcher match) is most prominent when all of the features (`upm`, `home_pitcher`, `run_diff`, `count_b-s`, and `inning_i`) are applied.

Balancing our data caused a notable decrease in the accuracy of our model, so we used feature selection to rank the importance of the features in the model without normalizing or resizing them first.

The coefficient of `upm` and the p-value changes as features were added to the model in order of rank importance. The below graphs illustrate that the `upm` coefficients increase and the p-values decrease as features are added. This shows that the effect of `upm`, in some cases, subtle though it may be, is significant as we control for other variables.

![UPM Significance vs. Number of Features for Overall Data](https://github.com/AshleyMcGee/MLB/blob/master/images/p_vs_nf_overall.png)

![UPM Coefficient vs. Number of Features Overall](https://github.com/AshleyMcGee/MLB/blob/master/images/upm_vs_nf_overall.png)

## Results

Overall, we were unable to reject the null hypothesis when looking at all of the data. We found there is no significant difference in the frequency of called strikes when the race of the home plate umpire and the pitcher are the same (p = 0.239).

We did, however, find a significant difference in whether strikes were called when the umpire and pitcher are both black. In that case, the umpire is 1.4 percent less likely to call a strike (p = 0.049).

![UPM Significance vs. Number of Features when Umpire is Black](https://github.com/AshleyMcGee/MLB/blob/master/images/p_vs_nf_black_umpire.png)

![UPM Coefficient vs. Number of Features when Umpure is Black](https://github.com/AshleyMcGee/MLB/blob/master/images/upm_vs_nf_black_umpire.png)

It is interesting to note that when the umpire and pitcher are both non-white, the umpire is 0.5 percent less likely to call a strike (p = 0.088).

![UPM Significance vs. Number of Features when Umpire is Non-white](https://github.com/AshleyMcGee/MLB/blob/master/images/p_vs_nf_nonwhite_umpire.png)

![UPM Coefficient vs. Number of Features when Umpure is Non-white](https://github.com/AshleyMcGee/MLB/blob/master/images/upm_vs_nf_nonwhite_umpire.png)

## Conclusions

When considering the overall data, we showed similar results to the results put forth by Parsons et al. They also did not discover a significant difference in the frequency of called strikes when the race of the umpire and pitcher matched, but, using linear-probability models, they had a lower p-value (p = 0.12).

But we found opposing results to the original research when looking at black and non-white matches between umpire and pitcher. Their results showed that when umpire and pitcher matched in race, umpires were more likely to call a strike, but we found black and non-white umpire/pitcher matches to be less likely to result in a called strike.

Overall, these results are not surprising. There were some marked differences between the Parsons et al. analysis and ours that could account for those differences. We performed a logistic regression whereas they used a linear regression model. Also, we used a different dataset covering different years (2013-2015 rather than 2004-2006). Changes in racial diversity, game rules, technology -- including electronic monitoring now in all stadiums of all games and calls -- and any number of unknown factors that we were not able to control for could have had an impact on the differences in our findings.
