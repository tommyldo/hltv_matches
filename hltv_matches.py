import cloudscraper
from bs4 import BeautifulSoup
import json


url = "https://www.hltv.org/matches"
scraper = cloudscraper.create_scraper()
response = scraper.get(url)

if response.status_code != 200:
    print(f"Failed to fetch page. Status code: {response.status_code}")
    exit()

soup = BeautifulSoup(response.text, "html.parser")
matches = soup.find_all(class_="match")

match_data = []

for match in matches:
    try:
        event = match.find(class_="match-event").get_text(strip=True)
        time =  match.find(class_="match-time").get_text(strip=True)
        format_ = match.find(class_="match-meta").get_text(strip=True)
        team_names = match.find_all(class_="match-teamname text-ellipsis")
        if len(team_names) < 2:
            continue
        team1 = team_names[0].get_text(strip=True)
        team2 = team_names[1].get_text(strip=True)

        match_entry = {
            "event": event,
            "format": format_,
            "match": f"{team1} vs {team2}",
            "time": time
        }
        match_data.append(match_entry)
    except Exception as e:
        continue

with open("hltv_matches.json", "w", encoding="utf-8") as f:
    json.dump(match_data, f, ensure_ascii=False, indent=2)

print("Saved structured match data to hltv_matches.json")
