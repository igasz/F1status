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

def fetch_data(endpoint):
    url = f"{BASE_URL}/{endpoint}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    

def show_combined_standings():
    drivers_data = fetch_data("driverStandings.json")
    constructors_data = fetch_data("constructorStandings.json")

    if not drivers_data or not constructors_data:
        print("Failed to fetch data.")
        return
    
    try:
        season = drivers_data['MRData']['StandingsTable']['season']
        drivers = drivers_data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
        constructors = constructors_data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']
    except (KeyError, IndexError):
        print("No standings data available for the current season.")
        return
    
    max_rows = max(len(drivers), len(constructors))

    title_left = f"F1 DRIVER STANDINGS (SEASON {season})"
    title_right = "F1 CONSTRUCTOR STANDINGS"

    print(f"\n{title_left:<58}   ||   {title_right}")
    
    sep_left = "-" * 58
    sep_right = "-" * 39
    print(f"{sep_left}   ||   {sep_right}")
    
    header_left = f"{'Pos.':<5} | {'Driver':<22} | {'Team':<16} | {'Points':<6}"
    header_right = f"{'Pos.':<5} | {'Team':<22} | {'Points':<6}"
    print(f"{header_left}   ||   {header_right}")
    
    print(f"{sep_left}   ||   {sep_right}")

    for i in range(max_rows):
        # empty
        row_left = " " * 58
        row_right = ""

        # drivers
        if i < len(drivers):
            d = drivers[i]
            pos = d['position']
            name = f"{d['Driver']['givenName']} {d['Driver']['familyName']}"
            team = d['Constructors'][0]['name']
            points = d['points']
            color = get_team_color(team)
            row_left = f"{pos:<5} | {name:<22} | {color}{team:<16}{RESET_COLOR} | {points:<6}"

        # teams
        if i < len(constructors):
            c = constructors[i]
            pos = c['position']
            team = c['Constructor']['name']
            points = c['points']
            color = get_team_color(team)
            row_right = f"{pos:<5} | {color}{team:<22}{RESET_COLOR} | {points:<6}"
        
        print(f"{row_left}   ||   {row_right}")

    # Bottom edge
    print(f"{sep_left}   ||   {sep_right}")

def get_next_race():
    data = fetch_data("next.json")
    
    if not data:
        return
    
    try:
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
    show_combined_standings()
    get_next_race()