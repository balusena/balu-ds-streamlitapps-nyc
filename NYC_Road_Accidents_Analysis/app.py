import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

DATA_URL = "NYC_Road_Accidents_Analysis/Motor_Vehicle.csv"

st.title("New York City - Road Accident Analysis")
st.markdown("Dashboard designed to analyze Road Accidents in New York City")

@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[['CRASH_DATE', 'CRASH_TIME']])
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    return data

data = load_data(15000)

st.header("Areas where most people are injured")
injured_people = st.slider("Number of persons injured ", 0, 19)
st.map(data.query("injured_persons >= @injured_people")[["LATITUDE", "LONGITUDE"]].dropna(how="any"))

st.header("Number of accidents occurring during a given time of the day")
hour = st.slider("Select Hour of the day", 0, 23)
data = data[data["CRASH_DATE_CRASH_TIME"].dt.hour == hour]
st.markdown("Road Accidents between %i:00 and %i:00" % (hour, (hour + 1) % 24))

midpoint = (np.average(data["LATITUDE"]), np.average(data["LONGITUDE"]))
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
            data=data[['CRASH_DATE_CRASH_TIME', 'LATITUDE', 'LONGITUDE']],
            get_position=["LONGITUDE", "LATITUDE"],
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
    st.subheader("Raw data by minute between %i:00 and %i:00" % (hour, (hour + 1) % 24))
    st.write(data)

st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour + 1) % 24))
filtered = data[
    (data["CRASH_DATE_CRASH_TIME"].dt.hour >= hour) & (data["CRASH_DATE_CRASH_TIME"].dt.hour < (hour + 1))
    ]
hist = np.histogram(filtered["CRASH_DATE_CRASH_TIME"].dt.minute, bins=60, range=(0, 60))[0]
chart_data = pd.DataFrame({"minute": range(60), "crashes": hist})

fig = px.bar(chart_data, x='minute', y='crashes', hover_data=['minute', 'crashes'], height=400)
st.write(fig)

st.header("Top 5 affected streets by class")
select = st.selectbox('Affected Class', ['Pedestrians', 'Cyclists', 'Motorists'])

if select == 'Pedestrians':
    st.write(data.query("injured_pedestrians >= 1")[["ON_STREET_NAME", "injured_pedestrians"]].sort_values(by=['injured_pedestrians'], ascending=False).dropna(how="any")[:5])

elif select == 'Cyclists':
    st.write(data.query("injured_cyclists >= 1")[["ON_STREET_NAME", "injured_cyclists"]].sort_values(by=['injured_cyclists'], ascending=False).dropna(how="any")[:5])
else:
    st.write(data.query("injured_motorists >= 1")[["ON_STREET_NAME", "injured_motorists"]].sort_values(by=['injured_motorists'], ascending=False).dropna(how="any")[:5])
       
