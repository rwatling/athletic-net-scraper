from playwright.sync_api import sync_playwright
import pandas as pd
import csv
import sys

# Arg parsing
if len(sys.argv) < 4:
    print("Usage: python scraper.py <team_id_csv> <year> <top n on team>")
    print("Example: python scraper.py section.in 2025 3")
    exit(0)

file_path = sys.argv[1]
year = sys.argv[2]
max_athletes = int(sys.argv[3])

# Read input csv file
team_dict={}
try:
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 2:
                key, value = row
                team_dict[key] = value
except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
    exit(1)
except Exception as e:
    print(f"An error occurred: {e}")
    exit(1)

# Populate running events
events = ['100', '200', '400', '800', '1600', '3200']
events = [ event + ' Meters' for event in events]
events.append('300m Hurdles - 30"')
events.append('100m Hurdles - 33"')
events.append('110m Hurdles - 39"')
events.append('300m Hurdles - 36"')

# For each team ID in the list of team IDs
conference_table = []
for team in team_dict.keys():
    url = f'https://www.athletic.net/team/{team}/track-and-field-outdoor/{year}/event-records'

    # Playwright to load dynamically populated tables
    # Playwright will wait until the page confirms it has loaded
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until='load')
        page.wait_for_selector('table')

        # Select table elements. In this case, it is all results for all events
        rows = page.query_selector_all('table tbody tr')
        table = []

        # For each row in the table, get the last 6 plaintext fields
        for row in rows:
            cols = row.query_selector_all('td')
            data = [col.inner_text().strip() for col in cols]
            table.append(data[-6:])

        # Convert table to dataframe to make use of iloc
        # Gather top 2 in each event and if time is null ignore result
        df = pd.DataFrame(table)
        for i in range(len(df)):
            if df.iloc[i,0] in events:
                for j in range(1,max_athletes+1):
                    if df.iloc[i+j][2]:
                        new_row = [df.iloc[i][0], df.iloc[i+j][0], df.iloc[i+j][2], team_dict[team]]
                        conference_table.append(new_row)
        browser.close()

# Assemble dataframe from conference table list and remove duplicates
conf_df = pd.DataFrame(conference_table)
conf_df = conf_df.drop_duplicates()
conf_df.columns = ['Event', 'Name', 'Time', 'School']

# Print dataframe by event sorted by Time as string which is a bit flaky
for event in events:
    print('*' * 80)
    print((conf_df[conf_df['Event'] == event].sort_values(by='Time')).to_string(index=False))
