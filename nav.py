from fasthtml.common import *
def get_navbar() :
    navbar = Article(Nav(Ul(
        Li((A("AutoTimeTable", href="/"))),
        Li(Details(Summary("Course"), Ul(
            Li(A("Add Course", href="/add/course")),
            Li(A("View Course", href="/view/course")),
          ), cls="dropdown")
        ),
        Li(Details(Summary("Schools"), Ul(
            Li(A("Add School", href="/add/school")),
            Li(A("View Schools", href="/view/schools")),
          ), cls="dropdown")
        ),
        Li(Details(Summary("Degrees"), Ul(
            Li(A("Add Degree", href="/add/degree")),
            Li(A("View Degrees", href="/view/degrees")),
        ), cls="dropdown")
           ),
        Li(Details(Summary("Student"), Ul(
            Li(A("Add Student", href="/add/student")),
            Li(A("View Student", href="/view/students")),
          ), cls="dropdown")
        ),
        Li(Details(Summary("Timetable"), Ul(
            Li(A("Add Timetable", href="/add/timetable")),
            Li(A("View Timetable", href="/view/timetable")),
        ), cls="dropdown")
           ),
        Li(Details(Summary("Electives"), Ul(
            Li(A("Add Elective", href="/add/electives")),
            Li(A("View Electives", href="/view/electives")),
        ), cls="dropdown")
           ),

    ),
        # style='''
        #   list-style-type: none;
        #   margin: 0;
        #   padding: 0;
        #   width: 15%;
        #   background-color: #f1f1f1;
        #   position: fixed;
        #   height: 100%;
        #   overflow: auto;
        # ''',
        id="navbar", name="navbar",
    ))
    return navbar