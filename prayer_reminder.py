import requests
import smtplib
from datetime import datetime

PASSWORD = "ymyv yjal yrny vvaq"
GMAIL = "thisismjeyz@gmail.com"
response = requests.get("http://muslimsalat.com/Layyah.json?key=c2969d2660f970d1cd45e78ead841867")
response.raise_for_status()

data = response.json()
print(data['items'][0])

# Use 24-hour format for comparison
current_time = datetime.now().strftime("%H:%M")

# Check if the current time is after Fajr prayer time
try:
    fajr_time = data['items'][0]['fajr']

    # Convert Fajr time to 24-hour format for comparison
    fajr_time_obj = datetime.strptime(fajr_time, "%I:%M %p")
    fajr_time_24 = fajr_time_obj.strftime("%H:%M")

    dhuhr_time_obj = datetime.strptime(data['items'][0]['dhuhr'], "%I:%M %p")
    dhuhr_time_24 = dhuhr_time_obj.strftime("%H:%M")

    asr_time_obj = datetime.strptime(data['items'][0]['asr'], "%I:%M %p")
    asr_time_24 = asr_time_obj.strftime("%H:%M")

    maghrib_time_obj = datetime.strptime(data['items'][0]['maghrib'], "%I:%M %p")
    maghrib_time_24 = maghrib_time_obj.strftime("%H:%M")

    isha_time_obj = datetime.strptime(data['items'][0]['isha'], "%I:%M %p")
    isha_time_24 = isha_time_obj.strftime("%H:%M")

    if current_time == fajr_time_24:
        print("It's time for Fajr prayer.")

        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=GMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=GMAIL,
                to_addrs="mudasirjamshaid0@gmail.com",
                msg=f"Subject:Prayer Times\n\nIt's time for prayer.Take a moment to disconnect from the world, and reconnect with the One who created it.")
    elif current_time == dhuhr_time_24:
        print("It's time for Dhuhr prayer.")

        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=GMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=GMAIL,
                to_addrs=GMAIL,
                msg=f"Subject:Prayer Times\n\n{data['items'][0]}")
    elif current_time == asr_time_24:
        print("It's time for Asr prayer.")

        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=GMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=GMAIL,
                to_addrs=GMAIL,
                msg="Subject:Prayer Times\n\nIt's time for prayer. Take a moment to disconnect from the world, and reconnect with the One who created it.".encode(
                    'utf-8'))
    elif current_time == maghrib_time_24:
        print("It's time for Maghrib prayer.")

        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=GMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=GMAIL,
                to_addrs=GMAIL,
                msg="Subject:Prayer Times\n\nIt's time for prayer. Take a moment to disconnect from the world, and reconnect with the One who created it.".encode(
                    'utf-8'))
    elif current_time == isha_time_24:
        print("It's time for Isha prayer.")

        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=GMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=GMAIL,
                to_addrs=GMAIL,
                msg="Subject:Prayer Times\n\nIt's time for prayer.Take a moment to disconnect from the world, and reconnect with the One who created it.".encode(
                    'utf-8'))
    else:
        print("No prayer time matches the current time.")

except Exception as e:
    print(f"An error occurred: {e}")
else:
    print("Message sent successfully.")
