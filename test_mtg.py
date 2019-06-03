import json
import re
from requests_html import HTMLSession
from mtg_scraper_utils import build_url_from_card_name

html_session = HTMLSession()

with open("my_collection.json", 'r') as f:
    collection = json.load(f)

for card in collection:
    url = build_url_from_card_name(card)
    print("Scraping: " + url)
    r = html_session.get(url)
    stats_text = r.html.find(".price-card-statistics-paper").pop().text
    paper_price_text = r.html.find(".price-box.paper").pop().text

    paper_price = float(re.findall("PAPER\n(.*)", paper_price_text).pop())
    stats_match_pattern = ".*Daily Change\n(.+).*\nWeekly Change\n(.+).*\nHighest Price\n(.+).*\nLowest Price\n(.+).*"
    stats_matches = re.findall(stats_match_pattern, stats_text).pop()
    stats_dict = dict(zip(["daily_change", "weekly_change", "highest_price", "lowest_price"], map(float, list(stats_matches))))
    card.update(stats_dict)
    card.update({"current_price": paper_price})
    card.update({"url": url})

print(json.dumps(collection, indent=4, sort_keys=True))
