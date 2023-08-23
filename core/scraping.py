import os
import django
django.setup()
import requests
from bs4 import BeautifulSoup
from core.models import Player
import time

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nbafantasy.settings")

# Configure Django settings
django.setup()

# Base URL for player lists
base_url = 'https://www.basketball-reference.com/players/'

# Initialize a list to store all player data
all_player_data = []

# Iterate through each letter of the alphabet
for letter in range(97, 123):  # ASCII codes for 'a' to 'z'
    letter_url = base_url + chr(letter)

    # Send an HTTP GET request to the letter's URL
    response = requests.get(letter_url)

    # Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the <tr> tags containing player data
        tr_tags = soup.find_all('tr')

        # Loop through each <tr> tag
        for tr_tag in tr_tags:
            strong_tag = tr_tag.find('strong')
            td_tags = tr_tag.find_all('td', class_='right')

            if strong_tag and td_tags:
                player_name = strong_tag.get_text(strip=True)
                year_min = int(td_tags[0].get_text(strip=True))
                year_max = int(td_tags[1].get_text(strip=True))

                # Split player name into first name and last name
                first_name, last_name = player_name.split(' ', 1)

                # Construct the player's gamelog URL for each year
                for year in range(year_min, year_max + 1):
                    url_letter = last_name[:1].lower()  # First letter of last name
                    player_url = f"https://www.basketball-reference.com/players/{url_letter}/{last_name[:5].lower()}{first_name[:2].lower()}01/gamelog/{year}"

                    player_data = {
                        'first_name': first_name,
                        'last_name': last_name,
                        'year': year,
                        'gamelog_url': player_url
                    }
                    all_player_data.append(player_data)

        # Introduce a delay to avoid aggressive scraping
        time.sleep(5)  # Wait for 5 seconds before the next request
    elif response.status_code == 403:
        print(f"Access to {letter_url} is forbidden.")
    else:
        print(f"Failed to access {letter_url}. Status code: {response.status_code}")

# Function to scrape game log data for a given player URL 
def scrape_player_gamelog(player_url):
    try:
        response = requests.get(player_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        player_name_element = soup.find('h1')
        player_name = player_name_element.text.strip()
        words = player_name.split()
        name = ' '.join(words[:2])
        season = words[2]

         # Player Image Url
        playerImage = soup.find('img', {'itemscope': 'image'})
        img_url = ''
        if playerImage:
            img_url = playerImage.get('src', '')
        
        # Extract game log table
        table = soup.find('table', {'id': 'pgl_basic'})

        if not table:
            return None

        # Extract game log rows
        rows = table.find_all('tr')

        gamelog_data = []

        # Skip header row
        for row in rows[1:]:
            data = row.find_all('td')

            # Extract desired columns from the row (e.g., date, points, rebounds, etc.)
            if data:
                if data[0].text.strip() != '':
                    games_played = data[0].text.strip()
                    date_game = data[1].text.strip()
                    team = data[3].text.strip()
                    opponent = data[5].text.strip()
                    #games_started = int(data[7].text.strip())
                    if data[7].text.strip() != 'inactive':
                        games_started_str = data[7].text.strip()
                        try:
                            games_started = int(games_started_str)
                        except ValueError:
                            games_started = 0  # or any other appropriate default value

                        if data[8].text.strip() != '': 
                            minutes_played_str = data[8].text.strip()
                            minutes, seconds = minutes_played_str.split(':')
                            minutes_played = float(minutes) + float(seconds) / 60
                        if data[9].text.strip() != '': 
                            field_goals_made = float(data[9].text.strip())
                        if data[10].text.strip() != '':
                            field_goals_attempted = float(data[10].text.strip())
                        if data[11].text.strip() != '':
                            field_goal_percentage = float(data[11].text.strip())
                        else:
                            field_goal_percentage = 0.0  # Provide a default value
                        if data[12].text.strip() != '':
                            three_pointers_made = float(data[12].text.strip())
                        else:
                            three_pointers_made = 0.0
                        if data[13].text.strip() != '':
                            three_pointers_attempted = float(data[13].text.strip())
                        else:
                            three_pointers_attempted = 0.0
                        if data[14].text.strip() != '':
                            three_point_percentage = float(data[14].text.strip())
                        else:
                            three_point_percentage = 0.0
                        if data[15].text.strip() != '':
                            free_throws_made = float(data[15].text.strip())
                        if data[16].text.strip() != '':
                            free_throws_attempted = float(data[16].text.strip())
                        free_throw_percentage = 0.0
                        if data[17].text.strip() != '':
                            free_throw_percentage = float(data[17].text.strip())
                        if data[18].text.strip() != '':
                            offensive_rebounds = float(data[18].text.strip())
                        if data[19].text.strip() != '':
                            defensive_rebounds = float(data[19].text.strip())
                        if data[20].text.strip() != '':
                            total_rebounds = float(data[20].text.strip())
                        if data[21].text.strip() != '':
                            assists = float(data[21].text.strip())
                        if data[22].text.strip() != '':
                            steals = float(data[22].text.strip())
                        if data[23].text.strip() != '':
                            blocks = float(data[23].text.strip())
                        if data[24].text.strip() != '':
                            turnovers = float(data[24].text.strip())
                        if data[25].text.strip() != '':
                            personal_fouls = float(data[25].text.strip())
                        if data[26].text.strip() != '':
                            points = float(data[26].text.strip())

                        # Create a new Player instance
                        player = Player(
                            img_url=img_url,        
                            name=name,
                            season=season,
                            date_game=date_game,  
                            team=team,
                            opponent=opponent,
                            games_played=games_played,  
                            games_started=games_started,
                            minutes_played=minutes_played,
                            field_goals_made=field_goals_made,
                            field_goals_attempted=field_goals_attempted,
                            field_goal_percentage=field_goal_percentage,
                            three_pointers_made=three_pointers_made,
                            three_pointers_attempted=three_pointers_attempted,
                            three_point_percentage=three_point_percentage,
                            free_throws_made=free_throws_made,
                            free_throws_attempted=free_throws_attempted,
                            free_throw_percentage=free_throw_percentage,
                            offensive_rebounds=offensive_rebounds,
                            defensive_rebounds=defensive_rebounds,
                            total_rebounds=total_rebounds,
                            assists=assists,
                            steals=steals,
                            blocks=blocks,
                            turnovers=turnovers,
                            personal_fouls=personal_fouls,
                            points=points
                        )

                        # Save the Player instance to the database
                        player.save()
    except requests.exceptions.RequestException as e:
        print(f"Error scraping {player_url}: {e}")

# Iterate through each player's gamelog URL
for player_data in all_player_data:
    scrape_player_gamelog(player_data['gamelog_url'])
    time.sleep(5)