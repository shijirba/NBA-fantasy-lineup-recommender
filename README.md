# NBA-fantasy-lineup-recommender

My aim of the project is to develop a web application where fantasy basketball managers can avail some intuitive visualizations and predictions which are otherwise only available via paid service from sports news companies. The problem which fantasy managers face is that most publicly available basketball statistics are in the tabular form with hundreds of numbers and do not support dynamic queries. For example, Figure 1 is from Yahoo sports fantasy application where I play shows the data in tabular form. I could say my inspiration came from below table. Because if we look at the second column, opponent, it shows the teams against Stephen Curry played. For example, on April 10th, Stephen Curry played against Portland Trail Blazers and scored 26 points, grabbed 5 boards and dished 7 assists. But how about the previous game statistics against Portland? Fantasy basketball managers have few spots through which he can draft players from free agent pool and would want to know how players available in the free agent pool performed against a particular team on upcoming schedule. 

![image](https://github.com/shijirba/NBA-fantasy-lineup-recommender/assets/78646055/59436566-0d29-42ae-b1fb-41559b455a5d)

_Figure 1. Stephen Curry game log in tabular form_

I want to solve this problem by enabling following three features on my web application and eventually helping managers choosing the right player from free agent pool.
-	Visualizing historical player performance against a particular team
-	Side by side player comparison 
-	Predicting a score player would put against a particular team 

My web application will be used by fantasy basketball managers and should help them make informed decision when deciding best possible lineup (who to start, who to bench), or choosing a player from free agent pool.
Second feature I proposed to implement is a side-by-side comparison of two players. As we can see from Figure 2, this feature is available for Yahoo’s plus service subscribed users. Fantasy manager’s search for choosing the right player from free agent pool usually comes down to last two players. So the table which displays this comparison will help managers greatly.

![image](https://github.com/shijirba/NBA-fantasy-lineup-recommender/assets/78646055/e5682aa9-cd05-494e-9710-494b7ad828f1)

_Figure 2. Side-by-side comparison_

The third feature I proposed to implement for the web application is to predict the points a given player would score against a particular team using long short term memory model which is one of the commonly used sport analytics algorithms.

Data
Django player and rank models are created to store player game log data and player rank respectively. Data is to be collected by a Python script that scrapes basketball-reference.com [4] and stores the statistics in SQLite. The data on aforementioned website is in the form of hundreds of spreadsheets as can be seen from Figure 3. As per Clause 5. Permitted Use of Terms of Use, it is stated that “Our guiding principles are that (1) sharing, using, modifying, repackaging, or publishing data found on individual SRL webpages is welcomed, whether for commercial or non-commercial purposes, but (2) any such sharing, use, modification, repackaging, or publication should explicitly credit SRL as the source of the data to the maximum extent possible and (3) any such sharing, use, modification, repackaging, or publication must not violate any express restrictions set forth in this Section 5, especially the restrictions set forth in subparts 5(i) and 5(j) below”. So the website has no clause forbidding web scraping.

![image](https://github.com/shijirba/NBA-fantasy-lineup-recommender/assets/78646055/9ac075be-9c0e-4afd-a120-1cc1518318ae)

Figure 3: Basketball-reference.com sports statistics come in this form.

There are two models used in my application which player and rank model. Player model as shown in Figure 4, are based on the Figure 3 table columns.
![image](https://github.com/shijirba/NBA-fantasy-lineup-recommender/assets/78646055/ebe2c35c-2d87-404f-9778-51d6df0a1bdf)

Figure 4: Django player model

Architecture
Application is being developed with Django, Chart.js, jQuery and Bootstrap and follows MVC pattern taught in Advanced web development module as shown in Figure 5 for web application feature 1 and 2. When user select a player name, team name and statistical category and presses on “Find”, values are retrieved into corresponding variables and then used to make AJAX request to the server endpoint. Endpoint “/find” will query the Player model to retrieve the game statistics data based on the selected player and team. The retrieved data is processed to separate out points, rebounds, assists, steals, and blocks for each game. The result is a JSON response containing this data, along with corresponding years for each game, and the selected statistics list (stats). This response will be used by the JavaScript code in the template to update the charts dynamically.

![image](https://github.com/shijirba/NBA-fantasy-lineup-recommender/assets/78646055/d970c9f5-69db-49e1-902c-8db54deefe5a)

Figure 5: MVC pattern applied in the application (Feature 1 and 2)

or the score prediction feature of my web application, I used three different models which are artificial neural network as a standard neural network, recurrent neural network and long short
term memory model as these deep-learning algorithms are used mostly for sequence processing. The model which produced the least MAE has been put into the production. Prediction function begins by querying a database to fetch historical game data for a player. Fetched data is then converted to a list of dictionaries and exported to a CSV file. The data is loaded from the CSV file in data frame in which game date column is converted to a datetime data type. The function then normalizes the game score using Min Max scaling. Sequences of game scores are created as training samples for the LSTM model. The model is built using Keras Sequential API which consist of a LSTM layer with 50 units and ReLU activation function, followed by dense output layer. It is trained using historical game data. It uses the mean absolute error as the loss function and the Adam optimizer. Training occurs over 20 epochs with batch size of 32. Prediction function returns the rounded predicted score as the JSON formatted string.

![image](https://github.com/shijirba/NBA-fantasy-lineup-recommender/assets/78646055/b3851b73-7f80-4a6c-8ebd-13fb36d265f5)

Figure 6: Player score prediction architecture (Feature 3)

Scraping function
Scraping function is the main component of my application. Coming up with scraping algorithm was a significant moment of my project. Issue was that the player data I wanted to sources was hosted on different URLs for each year player has played. The URL is in the following form.

<img width="511" alt="image" src="https://github.com/shijirba/NBA-fantasy-lineup-recommender/assets/78646055/8b6e321e-650e-4b89-9631-1c9008012eed">

Figure 7: Player data URL


The URL is formatted in a way that matches the structure used on the website for player game logs. There are 3 loops in the scraping algorithm. First loop iterates through each letter of the alphabet. For each letter, it constructs a URL (letter_url) by appending the letter to the base_url, which is the base URL of the website where player data is stored. An HTTP GET request is sent to the letter_url using the requests library. If the request is successful (status code 200), the script proceeds to scrape player data from the webpage. The BeautifulSoup library is used to parse the HTML content of the webpage. The script finds all <tr> tags (table rows) containing player data on the page. For each <tr> tag, it looks for a <strong> tag (for player names) and <td> tags with the class 'right' (for career start and end years). If both a <strong> tag and the desired <td> tags are found, it extracts the player's name, career start year (year_min), and career end year (year_max). The player's name is split into first name and last name. A loop iterates through each year within the player’s career, from year_min to year_max +1. For each year, it constructs a game log URL (player_url) by combining various components, including the first letter of the last name, a portion of the last name, a portion of the first name, and the year. Player data, including first name, last name, year, and game log URL, is organized into a dictionary (player_data). The player_data dictionary is appended to the all_player_data list, collecting data for multiple players and years. The result is a list (all_player_data) containing dictionaries for each player, each with information about the player's name, career years, and game log URLs.

Compare features works by querying player model to fetch data for the two specified players based on the values of two query parameters, playerName1 and playerName2 from the get request. It retrieves the rankings of the two players from the Rank model. For each player, it calculates the average values for five statistics: points, rebounds, blocks, steals and assists. The averages are rounded to one decimal place. The data for each player, including their statistics, image URL, and ranking is organized into dictionaries. JSON response provides a comparison of statistics between two players, along with their image URLs and rankings. Comparison is shown in Figure 10.


![image](https://github.com/shijirba/NBA-fantasy-lineup-recommender/assets/78646055/50bd0ac9-02be-476e-9725-c5554953f609)

Figure 10: Horizontal bar chart

![image](https://github.com/shijirba/NBA-fantasy-lineup-recommender/assets/78646055/127541f0-0ff4-4a72-9710-7caa4c6fab82)

Figure 11: Radar chart

![image](https://github.com/shijirba/NBA-fantasy-lineup-recommender/assets/78646055/ffd0bf74-d258-47c6-a052-bda5962aca04)

Figure 12: Final version which includes rank, prediction and average value




