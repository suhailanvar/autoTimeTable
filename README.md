# autoTimeTable
Automatic Timetable configurator for academic instiutions using FastHTML.
Primary objective is to reduce schedule clashes between subjects of different schools.

## Planned Features:
- Add subject list with course Id
- Add school list with school Id
- Add student list with selected subjects
- Add, Delete and Modify timetable manually
- Auto timetable
  - List of interschool subjects with most student selections sorted according to priority
  - Parameters
    - Total hours requried per subject
    - Staff avaialbility
    - Holidays

## Technology to be used:
FastHTML for the rendering and SQLite as the database.

## How to Run:
Just run ```python main.py``` in the terminal. 

If you have installed FastHTML correctly it should bring
up a local host link in the terminal. Copy and paste the link in your browser to see the webpage.

Add attribute ```port="your_port_number"``` in the ```serve()``` function in main.py to change the port number.

Use ```Ctrl + C``` to stop the server.