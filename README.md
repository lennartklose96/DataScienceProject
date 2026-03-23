# Data Science Project - Air Quality in Germany

In this project, we analyze trends in air quality in Germany from January 1, 2016, to March 1, 2026, focusing on the pollutants PM₁₀, PM₂.₅, and NO₂. The goal is to analyze trends and patterns in air pollution and to identify potential influencing factors. To this end, we examine temporal changes, regional differences, and the influence of specific events, weather conditions, and seasonal factors. We also compare different types of measurement station locations and, in some cases, place the results in an international context.



## Research Questions

- How did the average values of PM₁₀, PM₂.₅ and NO₂ change in Germany?
- How does air pollution in Germany behave around New Years?
- How did COVID-19 lockdowns and restrictions affect air pollution in Germany compared to the previous and following years?
- How does the air quality for PM₁₀ vary between the different german federal states?
- How does air pollution for PM₁₀ vary across urban, suburban and rural areas?
- How does air pollution vary between background, traffic and industrial monitoring stations?
- How do seasonal changes influence the pollution concentrations in Germany between 2016 and 2025?
- How did temperature and precipitation influence PM₁₀ and PM₂.₅ concentrations in major German cities between 2016 and 2025?
- How did summer school holidays in German federal states affect PM₁₀ and PM₂.₅ concentrations over the past ten years?
- How does Germany compare to other countries in terms of the daily and monthly average concentrations of PM₁₀, PM₂.₅ and NO₂?



## Data Pipeline

#### Collection

Our primary data source is the Umweltbundesamt API.
https://luftqualitaet.api.bund.dev/

We collected data from all of the 428 stations across Germany, initially requesting every single data point from the past ten years for our pollutants, which were PM₁₀, PM₂.₅ and NO₂. For this, each station returned a daily measurement, measured at 11:00 AM.

Then we found out more about the station attributes, such at the state they were in, or if they are a background or traffic station and divided our data for our different tasks accordingly, divided into different .csv files. This way we could answer our different research questions with differently formatted data, making it easier to work with.

Additional tasks required additional data sources such as the open-Meteo weather API and OpenAQ. Public dates for the summer school holidays in Germany were also used, simply copied from a table and put into a .csv, then filtered.

Links for additional data sources:
https://openaq.org/
https://open-meteo.com/en/docs
https://www.schulferien.org/

The pipeline for those was very similar. The main difference was that we had to request data in batches with wait timers, to not hit API limits, as the additional data sources had some restrictions. For that reason, when we gathered the weather data, we only used the location of the 100 largest german cities, and matched the station data for those cities with the geocoordinates used in open-Meteo.

#### Cleaning

For each research question, we formed the relevant daily/monthly/yearly mean average values of the pollution concentration. Those means were dependent on the task, for instance, the mean for all stations which measured in winter, or the mean of all background monitoring stations. 

Finally we kept .csv files with the aggregated data, containing a timestamp, the concentration value of the pollutants, and additional information such as the state, when applicable to the research question.



## Website

https://datascienceproject-deploy.onrender.com/

#### Building and Deploying

The website was developed using the Python framework Dash, as suggested by our supervisor. It was styled using some very basic css in Dash, the logic being entirely written in the code.

Deployment was realized with render. For this purpose, app.py is the main file that hosts the server, with the additional subpages being contained in the /pages folder. The application uses Gunicorn, a production-ready Python web server. Gunicorn handles incoming web requests from users, passes them to the Dash application for processing, and returns the results to the browser. The main branch of this repository is directly hosted on the website.

#### How to use

The website is mainly navigated using the navigation bar at the top. Here, users can find the different pages, with either more general information about the research project or the data, or jump straight to specific research questions. All the menu points that have an arrow selection lead to pages with a research question

The visualization for the research questions allow for interactive control. Here, users can select different attribute to change, such as to display daily, monthly or yearly mean values, or change the pollutants that are displayed. For some visualization, the time range can also be specified, either by a concrete year, or a slider that controls the start and end date. All the relevant selection boxes have a very short instruction above them, which should make it clear, what attribute is being selected. 

Beyond the selection menus, users can also click on the legend to hide certain values if wanted, or zoom into the visualization to highlight a specific area of the dataset.



## LLM usage

We acknowledge that LLMs were used to create (or assist creating) certain parts of the code.

The following list contains areas where LLMs were used, however, not every instance used an LLM, e.g., not every instance of filtering a data frame used LLM, only selected ones.

LLMs were primarily used for:

- Drafting initial versions of some visualizations
- Assisting with data frame filtering and manipulation
- Replicating and adapting page layouts across subpages

All code was reviewed, tested, and modified as needed to ensure correctness and alignment with our project goals.