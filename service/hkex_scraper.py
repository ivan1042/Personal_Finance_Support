import requests
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime, timedelta
import time
URL = "https://www3.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=hk"


def search_date(session, current_html, date):
    soup = BeautifulSoup(current_html, "html.parser")

    # Locate the form containing the date input.
    date_input = soup.find("input", attrs={"name": "txtShareholdingDate"})
    if date_input is None:
        raise ValueError(
            "Date input not found. Inspect the response for an error "
            "or access-challenge page."
        )

    form = date_input.find_parent("form")

    # Read fresh state from the page, rather than copying it from DevTools.
    payload = {
        element["name"]: element.get("value", "")
        for element in form.select('input[type="hidden"][name]')
    }

    # Preserve these fields even if they are not marked as hidden.
    for name in (
        "today",
        "sortBy",
        "sortDirection",
        "originalShareholdingDate",
        "alertMsg",
    ):
        element = form.find("input", attrs={"name": name})
        if element is not None:
            payload[name] = element.get("value", "")

    payload.update({
        "__EVENTTARGET": "btnSearch",
        "__EVENTARGUMENT": "",
        "txtShareholdingDate": date,
    })

    response = session.post(
        URL,
        data=payload,  # Form-encoded data, not json=payload
        headers={"Referer": URL},
        timeout=30,
    )
    response.raise_for_status()
    return response

def datetime_converter(date: str) -> datetime:

    return datetime.strptime(date, "%Y/%m/%d")

with requests.Session() as session:
    initial = session.get(URL, timeout=30)
    initial.raise_for_status()

    first_date = "2026/1/2"
    last_date = "2026/10/31"
    result = search_date(session, initial.text, first_date)

    location = Path(__file__).resolve().parent.parent / "data" / "hkex_to_hk_flow"
    # Save the response so you can inspect the actual returned table/date.
    full_path = location / f"hkex_test_{first_date}.html".replace("/", "_")

    with open(full_path, "w", encoding="utf-8") as file:
        file.write(result.text)

    soup = BeautifulSoup(result.text, "html.parser")
    heading = soup.select_one(".ccass-heading")

    print(
        "Result heading:",
        heading.get_text(" ", strip=True)
        if heading else "Not found — inspect hkex_test.html",
    )

    time.sleep(1)
    f_d = datetime_converter(first_date)
    l_d = datetime_converter(last_date)
    total_days = (l_d - f_d).days + 1
    delay = 5

    for day in range(total_days):
        new_date = f_d + timedelta(days=day)
        new = new_date.strftime("%Y/%m/%d")
        failure = False
        for k in range(3):
            time.sleep(delay * (k + 1))
            try:
                result = search_date(session, result.text, new)

                soup = BeautifulSoup(result.text, "html.parser")
                heading = soup.select_one(".ccass-heading")
                if heading is None:
                    raise ValueError(
                        "Unexpected page returned; stopping for inspection."
                    )
                print(
                    "Result heading:",
                    heading.get_text(" ", strip=True)
                    if heading else "Not found — inspect hkex_test.html",
                )

                full_path = location / f"hkex_test_{new}.html".replace("/", "_")

                with open(full_path, "w", encoding="utf-8") as file:
                    file.write(result.text)

                break

            except requests.HTTPError as exc:
                failure = True

        if failure:
            break

