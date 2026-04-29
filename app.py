# streamlit_india_weather.py
import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
import os
import folium
from streamlit_folium import st_folium

def get_lat_lon(place):
    geolocator = Nominatim(user_agent="india_weather_final")
    location = geolocator.geocode(place + ", India")
    if location is None:
        location = geolocator.geocode(place)
        if location is None:
            st.error("City or State not found in India. Please check spelling.")
            return None, None
    return location.latitude, location.longitude


def fetch_satellite_image(lat, lon):
    filename = f"satellite_{lat:.2f}_{lon:.2f}.jpg"
    if os.path.exists(filename):
        return Image.open(filename)
    
    url = (
        "https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?"
        "SERVICE=WMS&REQUEST=GetMap&VERSION=1.3.0"
        "&LAYERS=MODIS_Terra_CorrectedReflectance_TrueColor"
        "&FORMAT=image/jpeg&WIDTH=400&HEIGHT=400&CRS=EPSG:4326"
        f"&BBOX={lat-0.5},{lon-0.5},{lat+0.5},{lon+0.5}"
    )
    r = requests.get(url, timeout=15)
    if r.status_code != 200:
        st.warning("Could not fetch NASA satellite image.")
        return None
    
    img = Image.open(BytesIO(r.content)).convert("RGB")
    img.save(filename)
    return img

def interpret_wmo_code(code):
    mapping = {
        0: "Clear Sky", 1: "Mainly Clear", 2: "Partly Cloudy", 3: "Overcast",
        45: "Foggy", 48: " Rime Fog",
        51: "Light Drizzle", 53: " Moderate Drizzle", 55: " Dense Drizzle",
        61: "Slight Rain", 63: " Moderate Rain", 65: " Heavy Rain",
        71: "Slight Snow", 73: " Moderate Snow", 75: "Heavy Snow",
        80: "Slight Showers", 81: " Moderate Showers", 82: " Violent Showers",
        95: "Thunderstorm", 96: " Thunderstorm w/ Hail", 99: " Heavy Thunderstorm"
    }
    return mapping.get(code, "❓ Unknown")

def get_7day_weather(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        "&daily=weather_code,temperature_2m_max,temperature_2m_min,"
        "precipitation_sum,windspeed_10m_max,sunrise,sunset&timezone=auto"
    )
    r = requests.get(url, timeout=10)
    data = r.json().get("daily", {})

    forecast_results = []
    for i in range(len(data.get("time", []))):
        day_info = {
            "date": data["time"][i],
            "pattern": interpret_wmo_code(data["weather_code"][i]),
            "t_max": data["temperature_2m_max"][i],
            "t_min": data["temperature_2m_min"][i],
            "rain": data["precipitation_sum"][i],
            "wind": data["windspeed_10m_max"][i],
            "sunrise": data["sunrise"][i].split("T")[1],
            "sunset": data["sunset"][i].split("T")[1]
        }
        forecast_results.append(day_info)
    return forecast_results


st.set_page_config(page_title="India Weather & Satellite Viewer", layout="wide")
st.title(" India Weather & Satellite Viewer")

city_input = st.text_input("Enter an Indian City or State:", "")

if city_input:
    lat, lon = get_lat_lon(city_input)
    
    if lat and lon:
        st.subheader(f" Location: {city_input} (Lat: {lat:.2f}, Lon: {lon:.2f})")

        sat_img = fetch_satellite_image(lat, lon)
        if sat_img:
            st.image(sat_img, caption=f"NASA Satellite View: {city_input}", use_column_width=True)

        forecast = get_7day_weather(lat, lon)
        if forecast:
            st.subheader(" 7-Day Forecast")
            for day in forecast:
                st.write(f"**{day['date']}** | {day['pattern']} | Max: {day['t_max']}°C | Min: {day['t_min']}°C | "
                         f"Rain: {day['rain']}mm | Wind: {day['wind']}km/h | Sunrise: {day['sunrise']} | Sunset: {day['sunset']}")

            dates = [day['date'] for day in forecast]
            t_max = [day['t_max'] for day in forecast]
            t_min = [day['t_min'] for day in forecast]

            fig, ax = plt.subplots()
            ax.plot(dates, t_max, 'r-o', label='Max Temp')
            ax.plot(dates, t_min, 'b-o', label='Min Temp')
            ax.set_title(f"7-Day Temperature Forecast: {city_input}")
            ax.set_xlabel("Date")
            ax.set_ylabel("Temperature °C")
            ax.legend()
            plt.xticks(rotation=45)
            st.pyplot(fig)

        st.subheader(" City Map")
        m = folium.Map(location=[lat, lon], zoom_start=6)
        folium.Marker([lat, lon], popup=city_input).add_to(m)
        st_folium(m, width=700, height=500)