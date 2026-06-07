from datetime import datetime, time

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

LESSON_TIMES = [
    ("07:00", "07:50"),
    ("08:00", "08:45"),
    ("08:55", "09:40"),
    ("10:00", "10:45"),
    ("10:55", "11:40"),
    ("11:50", "12:35"),
    ("12:45", "13:30"),
    ("13:40", "14:25"),
    ("14:35", "15:20"),
    ("15:30", "16:15"),
]


def clean_subject(subject: str | None) -> str | None:
    if not subject:
        return None

    return subject.split(" |")[0].strip()


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data["bakalari"][entry.entry_id]

    entities = [
        BakalariSensor(
            coordinator,
            entry,
            "predmet",
            "Aktuální předmět"
        ),
        BakalariSensor(
            coordinator,
            entry,
            "ucitel",
            "Aktuální učitel"
        ),
        BakalariSensor(
            coordinator,
            entry,
            "mistnost",
            "Aktuální místnost"
        ),
        BakalariEndSensor(
            coordinator,
            entry
        ),
        BakalariNextLessonSensor(
            coordinator,
            entry
        ),
        BakalariStartOfDaySensor(
            coordinator,
            entry
        ),
        BakalariEndOfDaySensor(
            coordinator,
            entry
        )
    ]

    async_add_entities(entities)


class BaseBakalariEntity(
    CoordinatorEntity,
    SensorEntity
):

    _attr_should_poll = False
    _attr_has_entity_name = True

    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self.entry = entry

    def get_current_lesson(self):
        now = datetime.now()

        weekday_map = {
            0: "Pondělí",
            1: "Úterý",
            2: "Středa",
            3: "Čtvrtek",
            4: "Pátek"
        }

        day_name = weekday_map.get(now.weekday())

        if not day_name:
            return None

        timetable = self.coordinator.data

        if not timetable:
            return None

        lessons_today = timetable.get(day_name)

        if not lessons_today:
            return None

        current_index = None

        for i, (start, end) in enumerate(LESSON_TIMES):
            start_time = datetime.strptime(start, "%H:%M").time()
            end_time = datetime.strptime(end, "%H:%M").time()

            if start_time <= now.time() <= end_time:
                current_index = i
                break

        if current_index is None:
            return None

        try:
            lessons = lessons_today[current_index]

            if not lessons:
                return None

            return lessons[0]

        except Exception:
            return None

    def get_current_index(self):
        now = datetime.now()

        for i, (start, end) in enumerate(LESSON_TIMES):
            start_time = datetime.strptime(start, "%H:%M").time()
            end_time = datetime.strptime(end, "%H:%M").time()

            if start_time <= now.time() <= end_time:
                return i

        return None


class BakalariSensor(BaseBakalariEntity):

    def __init__(self, coordinator, entry, field, name):
        super().__init__(coordinator, entry)

        self.field = field
        self._attr_name = name
        self._attr_unique_id = f"{entry.entry_id}_{field}"

    @property
    def native_value(self):
        lesson = self.get_current_lesson()

        if not lesson:
            return None

        value = lesson.get(self.field)

        if self.field == "predmet":
            return clean_subject(value)

        return value


class BakalariEndSensor(BaseBakalariEntity):

    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)

        self._attr_name = "Konec aktuální hodiny"
        self._attr_unique_id = f"{entry.entry_id}_lesson_end"

    @property
    def native_value(self):
        index = self.get_current_index()

        if index is None:
            return None

        return LESSON_TIMES[index][1]


class BakalariNextLessonSensor(BaseBakalariEntity):

    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)

        self._attr_name = "Další předmět"
        self._attr_unique_id = f"{entry.entry_id}_next_subject"

    @property
    def native_value(self):
        now = datetime.now()

        weekday_map = {
            0: "Pondělí",
            1: "Úterý",
            2: "Středa",
            3: "Čtvrtek",
            4: "Pátek"
        }

        day_name = weekday_map.get(now.weekday())

        if not day_name:
            return None

        timetable = self.coordinator.data

        lessons_today = timetable.get(day_name)

        if not lessons_today:
            return None

        current_index = self.get_current_index()

        if current_index is None:
            return None

        next_index = current_index + 1

        if next_index >= len(lessons_today):
            return None

        lessons = lessons_today[next_index]

        if not lessons:
            return None

        return clean_subject(lessons[0].get("predmet"))


class BakalariStartOfDaySensor(BaseBakalariEntity):

    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)

        self._attr_name = "Začátek výuky dnes"
        self._attr_unique_id = f"{entry.entry_id}_start_of_day"

    @property
    def native_value(self):
        now = datetime.now()

        weekday_map = {
            0: "Pondělí",
            1: "Úterý",
            2: "Středa",
            3: "Čtvrtek",
            4: "Pátek"
        }

        day_name = weekday_map.get(now.weekday())

        if not day_name:
            return None

        timetable = self.coordinator.data

        if not timetable:
            return None

        lessons_today = timetable.get(day_name)

        if not lessons_today:
            return None

        first_index = None

        for i, lessons in enumerate(lessons_today):
            if lessons:
                first_index = i
                break

        if first_index is None:
            return None

        if first_index >= len(LESSON_TIMES):
            return None

        return LESSON_TIMES[first_index][0]

class BakalariEndOfDaySensor(BaseBakalariEntity):

    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)

        self._attr_name = "Konec výuky dnes"
        self._attr_unique_id = f"{entry.entry_id}_end_of_day"

    @property
    def native_value(self):
        now = datetime.now()

        weekday_map = {
            0: "Pondělí",
            1: "Úterý",
            2: "Středa",
            3: "Čtvrtek",
            4: "Pátek"
        }

        day_name = weekday_map.get(now.weekday())

        if not day_name:
            return None

        timetable = self.coordinator.data

        if not timetable:
            return None

        lessons_today = timetable.get(day_name)

        if not lessons_today:
            return None

        last_index = None

        for i in reversed(range(len(lessons_today))):
            if lessons_today[i]:
                last_index = i
                break

        if last_index is None:
            return None

        if last_index >= len(LESSON_TIMES):
            return None

        return LESSON_TIMES[last_index][1]