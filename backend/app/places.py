"""The places people travel between, and roughly how long the drive takes.

These are Rwanda's districts, except that Kigali city's three districts
(Nyarugenge, Gasabo, Kicukiro) count as one place, "Kigali", because that is
how buses and drivers name it. The landing-page map uses the same list.
"""

import math
from datetime import timedelta

PLACES = (
    "Kigali",
    "Bugesera",
    "Burera",
    "Gakenke",
    "Gatsibo",
    "Gicumbi",
    "Gisagara",
    "Huye",
    "Kamonyi",
    "Karongi",
    "Kayonza",
    "Kirehe",
    "Muhanga",
    "Musanze",
    "Ngoma",
    "Ngororero",
    "Nyabihu",
    "Nyagatare",
    "Nyamagabe",
    "Nyamasheke",
    "Nyanza",
    "Nyaruguru",
    "Rubavu",
    "Ruhango",
    "Rulindo",
    "Rusizi",
    "Rutsiro",
    "Rwamagana",
)

# Other names for the same place: Kigali's districts and main bus park, and
# the town names that bus companies still print on tickets.
ALIASES = {
    "nyarugenge": "Kigali",
    "gasabo": "Kigali",
    "kicukiro": "Kigali",
    "nyabugogo": "Kigali",
    "kigali city": "Kigali",
    "butare": "Huye",
    "gisenyi": "Rubavu",
    "ruhengeri": "Musanze",
    "cyangugu": "Rusizi",
    "kibuye": "Karongi",
    "byumba": "Gicumbi",
    "gitarama": "Muhanga",
    "kibungo": "Ngoma",
    "gikongoro": "Nyamagabe",
}

_BY_LOWER = {p.lower(): p for p in PLACES}


def normalise_place(name):
    """Return the official place name for `name`, or None if unknown."""
    if not name:
        return None
    key = " ".join(str(name).split()).lower()
    return _BY_LOWER.get(key) or ALIASES.get(key)


# Main town of each place (same points as the landing-page map, js/map.js).
TOWNS = {
    "Kigali": (-1.9441, 30.0619), "Bugesera": (-2.149, 30.093), "Burera": (-1.468, 29.835),
    "Gakenke": (-1.693, 29.784), "Gatsibo": (-1.62, 30.4), "Gicumbi": (-1.5763, 30.0675),
    "Gisagara": (-2.62, 29.82), "Huye": (-2.5967, 29.7394), "Kamonyi": (-2.004, 29.897),
    "Karongi": (-2.06, 29.348), "Kayonza": (-1.9, 30.509), "Kirehe": (-2.25, 30.67),
    "Muhanga": (-2.085, 29.756), "Musanze": (-1.499, 29.635), "Ngoma": (-2.159, 30.543),
    "Ngororero": (-1.865, 29.622), "Nyabihu": (-1.625, 29.542), "Nyagatare": (-1.297, 30.327),
    "Nyamagabe": (-2.4833, 29.5667), "Nyamasheke": (-2.3333, 29.0833),
    "Nyanza": (-2.352, 29.751), "Nyaruguru": (-2.64, 29.55), "Rubavu": (-1.702, 29.256),
    "Ruhango": (-2.223, 29.78), "Rulindo": (-1.728, 29.993), "Rusizi": (-2.484, 28.907),
    "Rutsiro": (-1.93, 29.37), "Rwamagana": (-1.949, 30.434),
}

# Roads wind through the hills: about 1.6 times the straight line, at an
# average of 45 km/h. Kigali to Huye comes out near 3 hours, Rusizi near 5.
ROAD_FACTOR = 1.6
AVERAGE_KMH = 45


def km_between(a, b):
    """Straight-line distance in km between two (lat, lng) points."""
    la1, lo1, la2, lo2 = map(math.radians, (*a, *b))
    h = (math.sin((la2 - la1) / 2) ** 2
         + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2)
    return 6371 * 2 * math.asin(math.sqrt(h))


def drive_time(a, b):
    """Rough driving time between two places, or two (lat, lng) points."""
    a, b = TOWNS.get(a, a), TOWNS.get(b, b)
    hours = km_between(a, b) * ROAD_FACTOR / AVERAGE_KMH
    return timedelta(minutes=math.ceil(hours * 4) * 15)  # to the next quarter hour
