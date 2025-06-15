import requests
import smtplib
from datetime import datetime
import time

PASSWORD = "ymyv yjal yrny vvaq"
GMAIL = "thisismjeyz@gmail.com"
TO_EMAIL = "mudasirjamshaid0@gmail.com"

def get_prayer_times():
    response = requests.get("http://muslimsalat.com/Layyah.json?key=c2969d2660f970d1cd45e78ead841867")
    response.raise_for_status()
    data = response.json()
    prayer_times = {
        "Fajr": data['items'][0]['fajr'],
        "Dhuhr": data['items'][0]['dhuhr'],
        "Asr": data['items'][0]['asr'],
        "Maghrib": data['items'][0]['maghrib'],
        "Isha": data['items'][0]['isha'],
    }
    return prayer_times

def convert_to_24(time_str):
    return datetime.strptime(time_str, "%I:%M %p").strftime("%H:%M")

def send_email(subject, body):
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=GMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=GMAIL,
                to_addrs=TO_EMAIL,
                msg=f"Subject:{subject}\n\n{body}"
            )
        print(f"✅ Email sent: {subject}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def main():
    sent_today = set()  # Prevent duplicate emails
    prayer_times = get_prayer_times()
    converted = {name: convert_to_24(t) for name, t in prayer_times.items()}
    print("Today's Prayer Times:", converted)

    while True:
        now = datetime.now().strftime("%H:%M")
        for prayer_name, prayer_time in converted.items():
            if now == prayer_time and prayer_name not in sent_today:
                message = "🕌 It's time for prayer. Take a moment to disconnect from the world, and reconnect with the One who created it."
                send_email(f"Prayer Reminder: {prayer_name}", message)
                sent_today.add(prayer_name)
        time.sleep(60)

if __name__ == "__main__":
    main()
