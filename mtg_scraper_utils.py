import re
import datetime


def encode_for_url_without_escapes(card_name):
    if card_name is None:
        raise ValueError("Shit's fucked, yo")
    _chars_to_remove = ["\'", ","]
    name_url = re.sub(" ", "+", card_name)
    name_url = re.sub("|".join(_chars_to_remove), "", name_url)
    return name_url


def build_url_from_card_name(card_dict):
    if card_dict is None:
        raise ValueError("Shit's fucked, yo")
    name_url = encode_for_url_without_escapes(card_dict.get("name")) + "#paper"
    set_url = encode_for_url_without_escapes(card_dict.get("set"))
    if card_dict.get("foil"):
        set_url += ":Foil"
    url = "/".join(["https://www.mtggoldfish.com/price/", set_url, name_url])
    return url


def scrape_and_update(collection):
    from requests_html import HTMLSession
    html_session = HTMLSession()
    updated = []
    # TODO: Make this parallellized somehow (multithreading with Queue? Or AsyncHTMLSession?)
    for card in collection:
        url = build_url_from_card_name(card)
        print("Scraping: " + url)
        r = html_session.get(url)

        # only continue scraping if page returns okay
        if r.status_code == 200:
            stats_text = r.html.find(".price-card-statistics-paper").pop().text
            paper_price_text = r.html.find(".price-box.paper").pop().text
            paper_price_text = paper_price_text.replace(",", "")  # remove comma from the pricey bois

            paper_price = float(re.findall("PAPER\n(.*)", paper_price_text).pop())
            stats_match_pattern = ".*Daily Change\n(.+).*\nWeekly Change\n(.+).*\nHighest Price\n(.+).*\nLowest Price\n(.+).*"
            stats_matches = re.findall(stats_match_pattern, stats_text).pop()
            stats_dict = dict(zip(["daily_change", "weekly_change", "highest_price", "lowest_price"],
                                  map(float, list(stats_matches))))

            # if current entries match the values scraped, don't bother updating
            if {k: card[k] for k in stats_dict.keys() if k in card} == stats_dict:
                updated.append(False)
            else:
                card.update(stats_dict)
                card.update({"current_price": paper_price})
                card.update({"url": url})
                card.update({"time_updated": datetime.datetime.today().strftime("%Y-%m-%d_%H:%M:%S")})
                card.update({"quantity": card.get("quantity", 1)})
                card.update({"purchase_price": card.get("purchase_price")})
                updated.append(True)
        else:
            print("[ERROR] bad request: %s" % url)
            updated.append(None)
    return updated
