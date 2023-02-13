## New York City - Road Accident Analysis 

## 1.Source
- The motor vehicle collision database includes the date and time, location (as borough, street names, zip code and latitude and longitude coordinates), injuries and fatalities, vehicle number and types, and related factors for all 8,77,181 collisions in New York City during 2015 and 2020.
- In this project we are performing analysis on Top 5 affected streets by classes such as 'Pedestrians', 'Cyclists', 'Motorists' numbers and time of accident.
- Technology and tools wise this project covers,
-    1.Python
-    2.Pydeck for Large-scale interactive data visualization in Python
-    3.Plotly for interactive data visualization
-    4.Numpy and Pandas for data cleaning
-    5.visual studio code and pycharm as IDE
-    6.Python Streamlit an open source app framework for our UI and https requests
-    7.Git and Github for our source code version control

## 2.Features
- Simple responsive UI
- Areas where most people are injured: Select Number of persons injured [ 0 =====> 19]
- Number of accidents occuring during a given time of the day: Select Hour of the day [ 0 ====> 23]
- Show raw data: Check the box [] to get Raw data by minute between specified time above 
- Minute vs Crashes plot: Breakdown by minute between specified time
- Top 5 affected streets by class:  Affected Class select from drop down [ 'Pedestrians', 'Cyclists', 'Motorists' ]
- Top 5 affected streets by class table showing street_name with total number of injuries

## 3.Usage
- Clone my repository here ===> ( https://github.com/balusena/balu-ds-streamlitapps-nyc/tree/main/NYC_Road_Accidents_Analysis)
- Open CMD in working directory.
- Run following command.
- pip install -r requirements.txt
- 'app.py' is the main Python file of Streamlit Web-Application. 
- To run app, write following command in CMD. or use any IDE.
- streamlit run app.py
- run the app app.py by logging into your streamlit account it works as intended when you follow the instruction stated in this document. 

## 4.Further work to be done
- The current implementation works well with the data we have used for building this application.
- Aiming to work with larger and real-world-NYC-Collisions-dataset and build an end to end application for New York City-Road Accident Analysis.
- Find a way to analyse the New York City - Road Accidents(I would be grateful if someone could help me on this project enhancement.)

<img src="https://github.com/balusena/balu-ds-streamlitapps-nyc/tree/main/NYC_Road_Accidents_Analysis/nyc.jpg">
