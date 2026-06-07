import json
import requests
from bs4 import BeautifulSoup


class BakalariApi:

    def __init__(self, url):
        self.url = url

    def fetch_timetable(self):
        headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/110.0.0.0 Safari/537.36"
            )
        }

        response = requests.get(self.url, headers=headers, timeout=15)
        response.encoding = "utf-8"

        soup = BeautifulSoup(response.text, "html.parser")

        timetable = {}

        day_names = [
            "Pondělí",
            "Úterý",
            "Středa",
            "Čtvrtek",
            "Pátek"
        ]

        rows = soup.select(".bk-timetable-row")

        for i, row in enumerate(rows):
            if i >= len(day_names):
                break

            day_name = day_names[i]
            timetable[day_name] = []

            cells = row.select(".bk-timetable-cell")

            for cell in cells:
                hour_lessons = []

                items = cell.select("[data-detail]")

                for item in items:
                    try:
                        raw_data = item.get("data-detail")
                        data = json.loads(raw_data)

                        lesson_info = {
                            "predmet": data.get("subjecttext", "???"),
                            "ucitel": data.get("teacher", ""),
                            "mistnost": data.get("room", ""),
                            "skupina": data.get(
                                "group",
                                "Celá třída"
                            ),
                            "cyklus": data.get(
                                "cycle",
                                "Každý týden"
                            )
                        }

                        hour_lessons.append(lesson_info)

                    except Exception:
                        continue

                timetable[day_name].append(hour_lessons)

        return timetable