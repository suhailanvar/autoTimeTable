from fasthtml.common import *
# from collated import *
from nav import get_navbar
from routes import register_routes

app, rt = fast_app(live=True)

db = database('data/timetable.db')

register_routes(app, rt, db)

students = db.t.student
Student = students.dataclass()
courses = db.t.course
Course = courses.dataclass()
degree = db.t.degree
Degree = degree.dataclass()

# app,rt, tbls, Tble = fast_app('data/buds.db', live=True, id=int, name=str, pk='id')

@rt('/')
def get():
    # add_toast(message="Toast is ready", typ="success")
    # students.insert(Student(name='Jane Doe'))
    page = Div(
            H1("AutoTimeTable", style="text-align:center;"),
            H3("Better TimeTables", style="text-align:center;"),
            P(  "Everything TimeTable. "
                "Navigate the menus in the header for the required functionalities. "),
            P("PS: This is a work in progress."),
            style="margin:auto; width:50%; text-align:center;"
        )
    return get_navbar() , page

@rt('/view/students')
def get():
    heading = "Student List"
    table = Table(
        Tr(Th('Roll No.'), Th('Name'), Th("Dob"), Th("")),
        *[(Tr(Td(o.id), Td(o.name), Td(o.degree_id),
              Td(A("Profile", href=f"/studentprofile/{o.id}")),
              Td(A("Edit", href=f"/studentedit/{o.id}")),
              Td(A("Delete", href=f"/studentdelete/{o.id}")))) for o in students()],
        id="student_display", name="student_display",

    )
    page = Titled(heading, table, style='margin:auto; width:50%;')
    return get_navbar(), page





serve(port=5252)