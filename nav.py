from fasthtml.common import *
def get_navbar() :
    navbar = Article(Nav(Ul(
        Li((A("AutoTimeTable", href="/"))),
        Li(Details(Summary("Course"), Ul(
            Li(A("Add Course", href="/addcourse")),
            Li(A("View Course", href="/view/course")),
          ), cls="dropdown")
        ),
        Li(Details(Summary("Schools"), Ul(
            Li(A("Add School", href="/addschool")),
            Li(A("View Schools", href="/view/schools")),
          ), cls="dropdown")
        ),
        Li(Details(Summary("Student"), Ul(
            Li(A("Add Student", href="/addstudent")),
            Li(A("View Student", href="/view/students")),
          ), cls="dropdown")
        ),
        Li(Details(Summary("Timetable"), Ul(
            Li(A("Add Timetable", href="/addtimetable")),
            Li(A("View Timetable", href="/view/timetable")),
        ), cls="dropdown")
           ),
        Li(Details(Summary("Electives"), Ul(
            Li(A("Add Elective", href="/addtimetable")),
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