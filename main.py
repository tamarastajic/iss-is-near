import datetime as dt
import requests
import smtplib
import time


# ---------------- Functions ----------------
def is_close():
    """A function that checks if ISS is close."""
    # ---------------- Calling ISS-Now API ----------------
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    # ---------------- Getting ISS-Now API Data ----------------
    data = response.json()
    iss_lat = float(data["iss_position"]["latitude"])
    iss_lang = float(data["iss_position"]["longitude"])

    # ---------------- Return If Close ----------------
    return MY_LAT - 5 <= iss_lat <= MY_LAT + 5 and MY_LONG - 5 <= iss_lang <= MY_LONG + 5


def is_night():
    """A function that checks if the sun set."""
    # ---------------- Calling Sunrise/Sunset API ----------------
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()

    # ---------------- Getting Sunrise/Sunset API Data ----------------
    data = response.json()["results"]
    sunrise = int(data["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["sunset"].split("T")[1].split(":")[0])

    # ---------------- Getting The Current Hour ----------------
    time_now = dt.datetime.now().hour

    # ---------------- Return If Night ----------------
    return time_now >= sunset or time_now <= sunrise


# ---------------- Constants ----------------

# Input your own data!
MY_LAT = YOUR LAT
MY_LONG = YOUR LONG
MY_EMAIL = YOUR EMAIL
MY_PASS = YOUR PASS
TO_EMAIL = TO EMAIL
# ---------------- Send an Email If Night and If ISS close ----------------

while True:
    if is_night() and is_close():
        connection = smtplib.SMTP("smtp.gmail.com", port=587)
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASS)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=TO_EMAIL,
            msg="Subject:Look up!\n\nISS is close"
        )
    time.sleep(60)
