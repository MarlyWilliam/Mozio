import requests
import json
import time

API_KEY = "6bd1e15ab9e94bb190074b4209e6b6f9"
BASE_URL = "https://api-testing.mozio.com/v2"


def search(
    start_address,
    end_address,
    mode,
    pickup_datetime,
    num_passengers,
    currency,
    campaign,
):
    url = f"{BASE_URL}/search/"
    headers = {"Api-Key": API_KEY, "Content-Type": "application/json"}
    data = {
        "start_address": start_address,
        "end_address": end_address,
        "mode": mode,
        "pickup_datetime": pickup_datetime,
        "num_passengers": num_passengers,
        "currency": currency,
        "campaign": campaign,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response


def poll(search_id):
    url = f"{BASE_URL}/search/{search_id}/poll/"
    headers = {"Api-Key": API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()


def book(
    search_id,
    result_id,
    email,
    phone_number,
    first_name,
    last_name,
    airline,
    flight_number,
):
    url = f"{BASE_URL}/reservations/"
    headers = {"Api-Key": API_KEY, "Content-Type": "application/json"}
    data = {
        "search_id": search_id,
        "result_id": result_id,
        "email": email,
        "phone_number": phone_number,
        "first_name": first_name,
        "last_name": last_name,
        "airline": airline,
        "flight_number": flight_number,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()


def book_poll(search_id):
    url = f"{BASE_URL}/reservations/{search_id}/poll/"
    headers = {"Api-Key": API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()


def cancel(confirmation_number):
    url = f"{BASE_URL}/reservations/{confirmation_number}"
    headers = {"Api-Key": API_KEY}
    response = requests.delete(url, headers=headers)
    return response.json()


def main():
    # Example search parameters
    start_address = "44 Tehama Street, San Francisco, CA, USA"
    end_address = "SFO: San Francisco, CA - San Francisco"
    mode = "one_way"
    pickup_datetime = "2023-12-01 15:30"
    num_passengers = 2
    currency = "USD"
    campaign = "Marly William"

    # Perform search
    search_response = search(
        start_address,
        end_address,
        mode,
        pickup_datetime,
        num_passengers,
        currency,
        campaign,
    )

    search_id = search_response.json()["search_id"]
    print("Search ID:", search_id)

    # Poll for search results after 5 seconds sleep to get results
    time.sleep(5)
    poll_results = poll(search_id)

    # Get the objects with provider_name = "Dummy External Provider"
    result = [
        result
        for result in poll_results["results"]
        for step in result["steps"]
        if step["details"]["provider_name"] == "Dummy External Provider"
    ]

    # Select the cheapest vehicle for "Dummy External Provider"
    cheapest_result = min(
        result, key=lambda x: float(x["total_price"]["total_price"]["value"])
    )
    result_id = cheapest_result["result_id"]
    print("Cheapest Result ID:", result_id)

    # Example booking parameters
    email = "happy_traveler@mozio.com"
    phone_number = "+201222825358"
    first_name = "Happyy"
    last_name = "Traveler"
    airline = "AA"
    flight_number = "123"

    # Book the cheapest vehicle
    book(
        search_id,
        result_id,
        email,
        phone_number,
        first_name,
        last_name,
        airline,
        flight_number,
    )

    # Booking poll for search results after 5 seconds sleep
    time.sleep(5)
    reservation_results = book_poll(search_id)

    reservation_number = reservation_results["reservations"][0]["id"]
    print("Booking Confirmed. Reservation Number:", reservation_number)
    print("Confirmation Number:", reservation_results["reservations"][0]["confirmation_number"])

    # Cancel the booking
    cancel_result = cancel(reservation_number)
    print(cancel_result)


if __name__ == "__main__":
    main()
