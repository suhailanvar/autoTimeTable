from fasthtml.common import *
from nav import *

# db = database('data/timetable.db')


# app,rt, tbls, Tble = fast_app('data/buds.db', live=True, id=int, name=str, pk='id')
app, rt = fast_app(live=True)


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

serve()