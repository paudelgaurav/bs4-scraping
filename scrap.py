import requests
import json

from typing import List
from bs4 import BeautifulSoup


def perform_scraping(url: str) -> List[str]:
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, features="lxml")
    # main table
    table = soup.find("table", id="sec235")
    body = table.find("tbody")
    rows = body.find_all("tr")

    banks = []

    for row in rows:
        bank = row.find("span").text
        banks.append(bank)

    assert banks[0] == "みずほ銀行"
    assert banks[-1] == "ゆうちょ銀行"

    return banks


def main():
    banks = perform_scraping("https://www.econtext.jp/bank_list/list.html")
    banks_dict = {"count": len(banks), "banks": banks}
    # Convering dict --> json
    banks_json = json.dumps(banks_dict, indent=4, ensure_ascii=False)

    # writing into banks.json file
    with open("banks.json", "w") as outfile:
        outfile.write(banks_json)

    print("Sucess")


if __name__ == "__main__":
    main()
