import requests
import os

os.system("")


BASE_URL = "https://api.jolpi.ca/ergast/f1/current"

TEAM_COLORS = {
    "red bull": "\033[38;2;54;113;198m",
    "mercedes": "\033[38;2;39;244;208m",
    "ferrari": "\033[38;2;232;0;32m",
    "mclaren": "\033[38;2;255;128;0m",
    "aston martin": "\033[38;2;34;89;61m",
    "alpine": "\033[38;2;253;75;199m",
    "williams": "\033[38;2;100;196;255m",
    "haas": "\033[38;2;230;0;43m",
    "sauber": "\033[38;2;0;223;89m",
    "rb": "\033[38;2;25;57;203m"
}

RESET_COLOR = "\033[0m"

def get_team_color(team_name):
    team_lower = team_name.lower()
    for key, color in TEAM_COLORS.items():
        if key in team_lower:
            return color
    return RESET_COLOR

def get_drivers_standing():
    url = f"{BASE_URL}/driverStandings.json"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        standings_list = data['MRData']['StandingsTable']['StandingsLists']

        if not standings_list:
            print("No standings data available for the current season.")
            return
        
        standings = standings_list[0]['DriverStandings']

        season = data['MRData']['StandingsTable']['season']

        print(f"\nF1 DRIVER STANDINGS (SEASON {season})")
        print("-" * 60)
        print(f"{'Pos.':<5} | {'Driver':<22} | {'Team':<16} | {'Points':<6}")
        print("-" * 60)

        for driver in standings:
            pos = driver['position']
            name = f"{driver['Driver']['givenName']} {driver['Driver']['familyName']}"
            team = driver['Constructors'][0]['name']
            points = driver['points']
            color = get_team_color(team)
            print(f"{pos:<5} | {name:<22} | {color}{team:<16}{RESET_COLOR} | {points:<6}")
        print("-" * 60)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching driver standings: {e}")

def get_constuctors_standing():
    url = f"{BASE_URL}/constructorStandings.json"

    try: 
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        standings_list = data['MRData']['StandingsTable']['StandingsLists']

        if not standings_list:
            return
        
        standings = standings_list[0]['ConstructorStandings']

        print(f"\nF1 CONSTRUCTOR STANDINGS")
        print("-" * 45)
        print(f"{'Pos.':<5} | {'Team':<22} | {'Points':<6}")
        print("-" * 45)

        for team_data in standings:
            pos = team_data['position']
            team = team_data['Constructor']['name']
            points = team_data['points']
            color = get_team_color(team)
            
            print(f"{pos:<5} | {color}{team:<22}{RESET_COLOR} | {points:<6}")
        print("-" * 45)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching constructor standings: {e}")


def get_next_race():
    url = f"{BASE_URL}/next.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        races = data['MRData']['RaceTable']['Races']
        
        if not races:
            print("\nNo upcoming races found. The season might have ended")
            return
        
        next_race = races[0]
        race_name = next_race['raceName']
        circuit = next_race['Circuit']['circuitName']
        country = next_race['Circuit']['Location']['country']

        date_str = next_race['date']
        time_str = next_race.get('time', 'TBD').replace('Z', ' UTC')

        print("\nNEXT RACE")
        print("-" * 55)
        print(f"Grand Prix: {race_name}")
        print(f"Circuit:    {circuit} ({country})")
        print(f"Date/Time:  {date_str} at {time_str}")
        print("-" * 55)
        print()

    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching next race details: {e}")

if __name__ == "__main__":
    get_drivers_standing()
    get_constuctors_standing()
    get_next_race()