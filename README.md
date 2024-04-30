# NBA-fantasy-lineup-recommender

My aim of the project is to develop a web application where fantasy basketball managers can avail some intuitive visualizations and predictions which are otherwise only available via paid service from sports news companies. The problem which fantasy managers face is that most publicly available basketball statistics are in the tabular form with hundreds of numbers and do not support dynamic queries. For example, Figure 1 is from Yahoo sports fantasy application where I play shows the data in tabular form. I could say my inspiration came from below table. Because if we look at the second column, opponent, it shows the teams against Stephen Curry played. For example, on April 10th, Stephen Curry played against Portland Trail Blazers and scored 26 points, grabbed 5 boards and dished 7 assists. But how about the previous game statistics against Portland? Fantasy basketball managers have few spots through which he can draft players from free agent pool and would want to know how players available in the free agent pool performed against a particular team on upcoming schedule. 

![image](https://github.com/shijirba/NBA-fantasy-lineup-recommender/assets/78646055/59436566-0d29-42ae-b1fb-41559b455a5d)
Figure 1. Stephen Curry game log in tabular form

I want to solve this problem by enabling following three features on my web application and eventually helping managers choosing the right player from free agent pool.
-	Visualizing historical player performance against a particular team
-	Side by side player comparison 
-	Predicting a score player would put against a particular team 

My web application will be used by fantasy basketball managers and should help them make informed decision when deciding best possible lineup (who to start, who to bench), or choosing a player from free agent pool.
Second feature I proposed to implement is a side-by-side comparison of two players. As we can see from Figure 2, this feature is available for Yahoo’s plus service subscribed users. Fantasy manager’s search for choosing the right player from free agent pool usually comes down to last two players. So the table which displays this comparison will help managers greatly.

![image](https://github.com/shijirba/NBA-fantasy-lineup-recommender/assets/78646055/e5682aa9-cd05-494e-9710-494b7ad828f1)
Figure 2. Side-by-side comparison
The third feature I proposed to implement for the web application is to predict the points a given player would score against a particular team using long short term memory model which is one of the commonly used sport analytics algorithms.
