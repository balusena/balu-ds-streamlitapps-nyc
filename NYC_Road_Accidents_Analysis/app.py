import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

DATE_TIME = "date/time"
DATA_URL = "NYC_Road_Accidents_Analysis/Motor_Vehicle.csv"

st.title("New York City - Road Accident Analysis")
st.markdown("Dashboard designed to analyze Road Accidents in New York City")

def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    
    # Parse dates with format MM/DD/YYYY HH:MM
    data["date/time"] = pd.to_datetime(data["CRASH_DATE"] + " " + data["CRASH_TIME"], format="%m/%d/%Y %H:%M")
    
    # Parse dates with format MM-DD-YY HH:MM
    alt_format = "%m-%d-%y %H:%M"
    alt_date_mask = data["CRASH_DATE"].str.contains("-", na=False)
    data.loc[alt_date_mask, "date/time"] = pd.to_datetime(data.loc[alt_date_mask, "CRASH_DATE"] + " " + data.loc[alt_date_mask, "CRASH_TIME"], format=alt_format)
    
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
    data.rename(columns=lambda x: str(x).lower(), inplace=True)
    
return data


data = load_data(15000)
data[['latitude', 'longitude']].to_csv("NYC_Road_Accidents_Analysis/lat_long.csv", index=False)

st.header("Areas where most people are injured")
injured_people = st.slider("Number of persons injured", 0, 19)
st.map(data.query("injured_persons >= @injured_people")[["latitude", "longitude"]].dropna(how="any"))

st.header("Number of accidents occurring during a given time of the day")
hour = st.slider("Select Hour of the day", 0, 23)
original_data = data
data = data[data["date/time"].dt.hour == hour]
st.markdown(f"Road Accidents between {hour}:00 and {(hour + 1) % 24}:00")

midpoint = (np.average(data["latitude"]), np.average(data["longitude"]))
st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,
    },
    layers=[
        pdk.Layer(
            "HexagonLayer",
            data=data[['date/time', 'latitude', 'longitude']],
            get_position=["longitude", "latitude"],
            auto_highlight=True,
            radius=100,
            extruded=True,
            pickable=True,
            elevation_scale=4,
            elevation_range=[0, 1000],
        ),
    ],
))

if st.checkbox("Show raw data", False):
    st.subheader(f"Raw data by minute between {hour}:00 and {(hour + 1) % 24}:00")
    st.write(data)

st.subheader(f"Breakdown by minute between {hour}:00 and {(hour + 1) % 24}:00")
filtered = data[(data["date/time"].dt.hour >= hour) & (data["date/time"].dt.hour < (hour + 1))]
hist = np.histogram(filtered["date/time"].dt.minute, bins=60, range=(0, 60))[0]
chart_data = pd.DataFrame({"minute": range(60), "crashes": hist})

fig = px.bar(chart_data, x='minute', y='crashes', hover_data=['minute', 'crashes'], height=400)
st.write(fig)

st.header("Top 5 affected streets by class")
select = st.selectbox('Affected Class', ['Pedestrians', 'Cyclists', 'Motorists'])

if select == 'Pedestrians':
    st.write(original_data.query("injured_pedestrians >= 1")[["on_street_name", "injured_pedestrians"]].sort_values(
        by='injured_pedestrians', ascending=False).dropna(how="any")[:5])
elif select == 'Cyclists':
    st.write(original_data.query("injured_cyclists >= 1")[["on_street_name", "injured_cyclists"]].sort_values(
        by='injured_cyclists', ascending=False).dropna(how="any")[:5])
else:
    st.write(original_data.query("injured_motorists >= 1")[["on_street_name", "injured_motorists"]].sort_values(
        by='injured_motorists', ascending=False).dropna(how="any")[:5])
