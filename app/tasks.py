from datetime import datetime, timedelta
import requests
from email.mime.text import MIMEText
import smtplib
import os

from django.conf import settings

from celery import shared_task
from jinja2 import Environment, FileSystemLoader

from app.models import City


def make_html_file(weather_data):
    file_loader = FileSystemLoader('app/templates')
    env = Environment(loader=file_loader)

    template = env.get_template('email_template.html')

    msg = template.render(city_name=weather_data['city_name'],
                          cur_weather=weather_data['cur_weather'],
                          humidity=weather_data['humidity'],
                          pressure=weather_data['pressure'],
                          wind=weather_data['wind'],
                          weather_description=weather_data['weather_description'])

    return msg


def email_send(user, weather_data):
    sender = os.getenv("sender")
    password = os.getenv("password")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    template = make_html_file(weather_data)

    server.login(sender, password)
    msg = MIMEText(f"{template}", "html")
    msg["From"] = sender
    msg["To"] = user.email
    msg["Subject"] = "Weather"
    server.sendmail(sender, user.email, msg.as_string())


def get_weather(city):
    try:
        r = requests.get(
            settings.REQUESTS_GET_WEATHER.replace('city_name', city.name)
        )
        data = r.json()

        city_name = data['name']
        cur_weather = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        weather_description = data['weather'][0]['description']

        weather_data = {
            'city_name': city_name,
            'cur_weather': cur_weather,
            'humidity': humidity,
            'pressure': pressure,
            'wind': wind,
            'weather_description': weather_description,

        }

        return weather_data
    except:
        City.objects.filter(id=city.id).delete()


@shared_task()
def send_email_weather():
    cities = City.objects.all()
    for city in cities:
        dt = datetime.now()
        next_sent = city.time_sent
        if next_sent == None:
            next_sent = dt

        if next_sent.strftime('%Y.%m.%d %H:%M') <= dt.strftime('%Y.%m.%d %H:%M'):
            weather_data = get_weather(city)

            if weather_data != None:
                email_send(city.user, weather_data)
                hours = int(city.notification_interval)
                new_data = dt + timedelta(hours=hours)
                city.time_sent = new_data
                city.save()
