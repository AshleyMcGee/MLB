# Examining Potential Umpire Bias in Major League Baseball

We started with review of research done by Christopher A. Parsons, Johan Sulaeman, Michael C. Yates, and Daniel S. Hamermesh on potential racial bias exhibited by umpires in Major League Baseball in 2004-2006. In short, their research stated that when the race of the umpire matched the race of the starting pitcher, the umpire was more likely to call a strike. Additionally, this particular effect was only seen in stadiums where there was no electronic review of the calls made by umpires. In 2004-2006, approximately 35% of games had electronic monitoring of calls.

## Our Data

We scraped every pitch of every game of the 2013, 2014, and 2015 MLB seasons from [Baseball-Reference.com](https://www.baseball-reference.com).

We created code to retrieve from each game, based on the structure of each game's Play by Play table:
* Home plate umpire name
* Pitch sequence
* Pitcher name for each plate appearance
* Batter name for each plate appearance
* Inning of each plate appearance
* Score of the game during each plate appearance

Once we scraped this data from Baseball-Reference, we transformed it to:
* Show the count of balls and strikes before each pitch
* Have only one row for each pitch
* Drop rows whose pitches were not solely dependent on the home plate umpire's discretion -- that is, we kept only rows with called strikes and called balls (not intentional balls, pitchouts, etc.). These rows corresponded with pitch code C (called strike) or B (called ball).

With each relevant pitch on its own row, we then added the race of each pitcher and umpire included in the 2013-15 game data. We compiled this data by starting with an Excel file of an MLB "player census" done by [BestTickets.com](www.besttickets.com/blog/mlb-players-census/). This Excel file only included players on each team's Opening Day roster for the 2014 season, so we then manually identified any pitchers not in the initial player census using a Google Image Search. Fortunately, the BestTickets file classified players into four groups: white, black, Hispanic, or Asian. These groups matched those used in the Parsons et al. study. For umpires, we again used a Google Image Search to determine each umpire's race (sorted into the same four categories as players). For pitchers and umpires whose race was not immediately obvious to the initial evaluator after a search, other group members were asked to provide a second opinion.  Batter data helped separate each plate appearance (and therefore helped determine the ball-strike count for each pitch), but it was dropped once it was no longer needed.

When we finally had race data for all pitchers and umpires, we merged it with the game data. From there, we were able to one-hot encode the data into the necessary columns:
* `strike_given_called`: Whether the pitch was called a strike
* `upm`: Whether the umpire and pitcher race matched for that pitch
* `home_pitcher`: Whether the pitcher was pitching for the home team
* `run_diff`: The run difference for the pitcher's team at that point in the game; for example, if the pitcher's team led by 5 runs, this was 5, and if the team trailed by 4 runs, this was -4. If the game was tied, this was 0.
* `count_b-s`: Where `b` is the number of balls in the count and `s` is the number of strikes in the count.
* `inning_i`: Where `i` is the inning in which the pitch was thrown. If a pitch was thrown in extra innings, it was placed in the `inning_9` column.

At this point, the data was ready to be tested in models.

## Our Hypothesis

There will be a difference in the number strikes called when the race of the home plate umpire matches the race of he pitcher.

Null: There will be not be any difference in the number of strikes called when the race of the home plate umpire matches the race of the pitch.

## Our Analysis

Logistic Regression was performed to evaluate the potential effects of umpire and pitcher race on the whether or not there were called balls or strikes.

After some testing with the model, we found that the significance of UPM is most prominent when all of the features are in.

Balancing our data caused a notable decrease in the accuracy of our model. So we used feature selection to rank the importance of the features in the model without normalizing or resizing them first.

The coefficient of UPM and the p-value changes as you add features to the model in order of rank-importance. The below graphs illustrate that the UPM coefficients increase and the p-values decrease as features are added, This shows that the effect of UPM, in some of cases, subtle though it may be, is significant as we control for other variables.

![UPM p-value vs number of features](https://github.com/AshleyMcGee/MLB/blob/master/images/pval_vs_nfeatures_all.png)

![UPM coefficient vs number of features](https://github.com/AshleyMcGee/MLB/blob/master/images/upm_vs_nfeatures_all.png)

## Results

Overall, we were unable to reject the null hypothesis, meaning that we cannot say that called strikes made by umpires is impacted by the race of the umpire or the pitcher.

However, when using fixed effects when the umpire was black there was a p value of .049, suggesting....

Furthermore, when using fixed effects where the umpire was 'non-white' (black or hispanic) there was a p value of .088. And when using fixed effects where the pitcher was 'non-white' (asian, black, or hispanic) there was a p value of .063. While this does not fall under the more desirable 95% confidence it does fall under 90% confidence and is an interesting finding.

## Conclusions