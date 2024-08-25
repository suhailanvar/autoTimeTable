from .timetable import register_timetable
from .electives import register_electives
from .school import register_school
from .degree import register_degree

def register_routes(app, rt, db):
    register_timetable(app, rt, db)
    register_electives(app, rt, db)
    register_school(app, rt, db)
    register_degree(app, rt, db)
