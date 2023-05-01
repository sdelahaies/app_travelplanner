# app_travelplanner

## docker install:

in your DST VM run the commands
```
docker pull sdelahaies/app-travelplanner:latest
docker run -p 8050:8050 sdelahaies/app-travelplanner
```
the app is available at `your.VM.ip.address:8050/travel_planner`

## Travel Planner

to test the app

1. select VALROMEY SUR SERAN in the dropdown menu

2. click on `let's find the points of interest!`

3. click on `Let's plan our journey!` and scroll down to see the daily plans 

remark: if you go to `your.VM.ip.address:8050/` you get the login page, you can access the app with the credentials 
```
username = travel
password = planner
```
then click on the link.