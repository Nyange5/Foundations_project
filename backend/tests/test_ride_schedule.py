"""A driver can't post rides they couldn't physically make."""

from datetime import datetime, timedelta

from app.places import drive_time
from app.validation import local_now


def post(client, headers, offer_id, origin, destination, departure, **extra):
    vehicle_id = client.get("/api/drivers/vehicles", headers=headers).get_json()["vehicles"][0][
        "vehicle_id"]
    return client.post("/api/rides", headers=headers, json={
        "vehicle_id": vehicle_id, "origin": origin, "destination": destination,
        "ride_type": "private", "departure_time": departure.isoformat(), "price": 30000,
        "pickup_point": "Nyabugogo bus park, gate 2", **extra})


def first_departure(client, headers):
    rides = client.get("/api/drivers/rides", headers=headers).get_json()["rides"]
    return datetime.fromisoformat(rides[0]["departure_time"])


def test_drive_times_are_realistic():
    assert drive_time("Kigali", "Kigali") == timedelta(0)
    assert timedelta(hours=2) <= drive_time("Kigali", "Huye") <= timedelta(hours=4)
    assert drive_time("Kigali", "Rusizi") > drive_time("Kigali", "Huye")


def test_same_route_twice_the_same_morning_is_refused(client, ride):
    # The fixture's ride: Kigali to Huye, 30 minutes from now.
    headers, offer_id = ride(minutes_ahead=30)
    start = first_departure(client, headers)

    clash = post(client, headers, offer_id, "Kigali", "Huye", start + timedelta(hours=3))

    assert clash.status_code == 409
    assert clash.get_json()["error"]["code"] == "schedule_clash"
    assert "earliest you could leave Kigali" in clash.get_json()["error"]["message"]


def test_return_trip_after_arriving_is_allowed(client, ride):
    headers, offer_id = ride(minutes_ahead=30)
    start = first_departure(client, headers)
    back = start + drive_time("Kigali", "Huye") + timedelta(minutes=30)

    assert post(client, headers, offer_id, "Huye", "Kigali", back).status_code == 201
    # And then Kigali to Huye again once they are back.
    again = back + drive_time("Huye", "Kigali") + timedelta(minutes=30)
    assert post(client, headers, offer_id, "Kigali", "Huye", again).status_code == 201


def test_ride_before_another_must_leave_time_to_get_there(client, ride):
    headers, offer_id = ride(minutes_ahead=24 * 60)  # Kigali to Huye tomorrow
    start = first_departure(client, headers)

    # Rusizi to Kigali arriving too late for the Kigali departure.
    late = post(client, headers, offer_id, "Rusizi", "Kigali", start - timedelta(hours=2))
    assert late.status_code == 409
    assert "To make both" in late.get_json()["error"]["message"]

    early = start - drive_time("Rusizi", "Kigali") - timedelta(minutes=30)
    assert post(client, headers, offer_id, "Rusizi", "Kigali", early).status_code == 201


def test_other_drivers_rides_do_not_count(client, ride):
    ride(minutes_ahead=30)
    headers, offer_id = ride(minutes_ahead=6 * 60)
    start = first_departure(client, headers)

    assert post(client, headers, offer_id, "Huye", "Kigali",
                start + drive_time("Kigali", "Huye") + timedelta(hours=1)).status_code == 201


def test_driver_too_far_away_is_refused(client, ride):
    headers, offer_id = ride(minutes_ahead=3 * 24 * 60)
    in_rusizi = {"lat": -2.484, "lng": 28.907}

    soon = post(client, headers, offer_id, "Kigali", "Musanze",
                local_now() + timedelta(hours=1), current_location=in_rusizi)
    assert soon.status_code == 409
    assert soon.get_json()["error"]["code"] == "cannot_reach"

    later = post(client, headers, offer_id, "Kigali", "Musanze",
                 local_now() + timedelta(hours=7), current_location=in_rusizi)
    assert later.status_code == 201


def test_without_a_location_only_the_schedule_is_checked(client, ride):
    headers, offer_id = ride(minutes_ahead=3 * 24 * 60)

    assert post(client, headers, offer_id, "Rusizi", "Kigali",
                local_now() + timedelta(hours=1)).status_code == 201
