from fasthtml.common import *
# from collated import *
from nav import get_navbar

app, rt = fast_app(live=True)

db = database('data/timetable.db')

students = db.t.student
Student = students.dataclass()
courses = db.t.course
Course = courses.dataclass()
elected_courses = db.t.elected_courses
Elected_course = elected_courses.dataclass()
degree = db.t.degree
Degree = degree.dataclass()
timetable = db.t.timetable
Timetable = timetable.dataclass()
timetable2 = db.t.timetable2
Timetable2 = timetable2.dataclass()

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

def get_electives_row() :
    query1 = f'''
        select s.*, d.name
        from student s inner join degree d on d.id = s.degree_id;
    '''

    student_list = [x for x in db.execute(query1)]

    for student in student_list :
        # elective_list = [x for x in db.execute(query2.replace('1', str(student[0])))]
        query2 = f'''
                select e.student_id, e.course_type, e.course_id, c.name
               from {elected_courses} as e inner join {courses} as c on e.course_id = c.id
                where e.student_id = {student[0]}
                order by e.course_type desc, c.name;
            '''
        elective_list = [x for x in db.execute(query2)]
        pe = [Td(x[3]) for x in elective_list if x[1] == 'PE']
        oe = [Td(x[3]) for x in elective_list if x[1] == 'OE']
        # print(elective_list)
        yield Tr(Td(student[0]), Td(student[1]), Td(student[3]),
                 pe[0] if len(pe)>0 else Td(""), pe[1] if len(pe)>1 else Td(""), pe[2] if len(pe)>2 else Td(""),
                 oe[0] if len(oe)>0 else Td(""), oe[1] if len(oe)>1 else Td(""), oe[2] if len(oe)>2 else Td(""))
                 # *pe, *oe)

@rt('/view/electives/')
def get(year:str="2024", sem:str="3"):
    heading = f"Elective List | {year} | Semester {sem}"
    table = Table(
        Tr(Th('Roll No.'), Th('Name'), Th("Degree"), Th("PE1"), Th("PE2"), Th("PE3")
           , Th("OE1"), Th("OE2"), Th("OE3")),
        *[x for x in get_electives_row()],
        id="student_display", name="student_display",
    )

    # Divide the report further into PE and OE versions
    query = f'''
        select c.name, count(c.name)
        from {elected_courses} as e inner join {courses} as c on e.course_id = c.id
        group by c.name
        order by count(c.name) desc;
    '''
    sub_selection_count = [x for x in db.execute(query)]
    subject_selection_report = Div( H3("Subject Selection Report"),
        Table(
        *[Tr(Td(x[0]), Td(x[1])) for x in sub_selection_count],
    ), style="margin:auto; width:50%;")

    page = Titled(heading, table, style='margin:auto; width:70%;')
    return get_navbar(), page, subject_selection_report

@rt('/view/timetable/')
def get(year:str="2024", sem:str="3", degree:str="Msc MI"):

    course_list = [x.name for x in courses()]
    print(course_list)
    heading = f"Timetable | {year} | Semester {sem} | {degree}"
    # table1 = Table(
    #     Tr(Th('Time'), Th('Monday'), Th("Tuesday"), Th("Wednesday"), Th("Thursday"),
    #        Th("Friday"), Th("Saturday"), Th("Sunday")),
    #     *[Tr(Td(x.time),
    #          Td(course_list[x.mon]), Td(course_list[x.tue]),
    #          Td(course_list[x.wed]), Td(course_list[x.thu]),
    #          Td(course_list[x.fri]), Td(course_list[x.sat])) for x in timetable(where="year='2024' and sem='3' and degree_id=1")],
    #     id="student_display", name="student_display",
    #
    # )

    time_list = [x.time for x in timetable(where="year='2024' and sem='3' and degree_id=1")]
    ttble = timetable(where="year='2024' and sem='3' and degree_id=1")

    table2 = Table(
        Tr(Th('Day'), *([Th(x) for x in time_list])),
        # *[Tr(Td(x), *[Td(y.mon) for y in timetable(where="year='2024' and sem='3' and degree_id=1")])
        #   for x in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']],
        Tr(Td('Monday'), *[Td(course_list[x.mon]) for x in ttble]),
        Tr(Td('Tuesday'), *[Td(course_list[x.tue]) for x in ttble]),
        Tr(Td('Wednesday'), *[Td(course_list[x.wed]) for x in ttble]),
        Tr(Td('Thursday'), *[Td(course_list[x.thu]) for x in ttble]),
        Tr(Td('Friday'), *[Td(course_list[x.fri]) for x in ttble]),
        Tr(Td('Saturday'), *[Td(course_list[x.sat]) for x in ttble]),
        Tr(Td(A("Edit", href="/view/timetable/edit"), colspan=10)),
        id="student_display", name="student_display",

    )
    # Using CSS to transpose table1. Need to find a better way of applying styles.
    # table3 = Table(
    #     Tr(Th('Time', style="display: block;"), Th('Monday', style="display: block;"),
    #        Th("Tuesday", style="display: block;"), Th("Wednesday", style="display: block;"),
    #        Th("Thursday", style="display: block;"), Th("Friday", style="display: block;"),
    #        Th("Saturday", style="display: block;"),
    #        style="display: block; float: left;"),
    #     *[Tr(Td(x.time),
    #          Td(course_list[x.mon], style="display: block;"), Td(course_list[x.tue], style="display: block;"),
    #          Td(course_list[x.wed], style="display: block;"), Td(course_list[x.thu], style="display: block;"),
    #          Td(course_list[x.fri], style="display: block;"), Td(course_list[x.sat], style="display: block;"),
    #          style="display: block; float: left;") for x in timetable(where="year='2024' and sem='3' and degree_id=1")],
    #     id="student_display", name="student_display",
    # )

    page = Titled(heading, table2,Br(), style='margin:auto; width:70%;')
    return get_navbar(), page

def get_dropdown(course_list, current_value, day, time, rowid) :

    # if day == 'mon' : t.mon = current_value
    # elif day == 'tue' : t.tue = current_value
    # elif day == 'wed' : t.wed = current_value
    # elif day == 'thu' : t.thu = current_value
    # elif day == 'fri' : t.fri = current_value
    # elif day == 'sat' : t.sat = current_value
    # t.time = time
    # t.year = "2024"
    # t.sem = "3"
    # t.degree_id = 1
    # print(t)

    dropdown = Select(
        *[Option(x, value=course_list.index(x), selected=(True if x == course_list[current_value] else False)) for x in course_list],
        name=f"{day}", id=f"{day}"
    )

    cont = Form(dropdown,
                Hidden(name="time", value=time),
                # Hidden(name="cur_val", value=current_value),
                # Hidden(name="day", value=day),
                Hidden(name="id", value=rowid),
                A("Change", hx_post="/view/timetable/edit/"))
    print("Course list index", course_list.index("Computer Vision"))

    return cont


def get_td_template(course_list, collist, x, y, i) :
    cont = Td(course_list[x[collist[y+i]]], A("Edit",
                        hx_put=f"/view/timetable/edit/?day={collist[y+i]}&time={x["time"]}&cur_val={x[collist[y+i]]}&rowid={x["id"]}",
                                                         hx_target=f"#edit_main-{i}{x["id"]}", hx_swap="outerHTML"),
                         id=f"edit_main-{i}{x["id"]}")
    return cont

@rt('/view/timetable/edit')
def get(year:str="2024", sem:str="3", degree:str="Msc MI"):
    course_list = [x.name for x in courses()]
    time_list = [x.time for x in timetable(where="year='2024' and sem='3' and degree_id=1")]
    ttble = timetable(where="year='2024' and sem='3' and degree_id=1", as_cls=False)

    t = Timetable()
    collist = [x.name for x in timetable.columns]
    y = 5

    table2 = Form(Table(
        Tr(Th('Day'), *([Th(x) for x in time_list])),
        *[Tr(Td(z), *[get_td_template(course_list, collist, x, y, i) for x in ttble])
          for i, z in enumerate(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])],
        # Tr(Td('Monday'), *[Td(x[collist[5]]) for x in ttble]),
        # Tr(Td('Tuesday'), *[Td(course_list[x.tue]) for x in ttble]),
        # Tr(Td('Wednesday'), *[Td(course_list[x.wed]) for x in ttble]),
        # Tr(Td('Thursday'), *[Td(course_list[x.thu]) for x in ttble]),
        # Tr(Td('Friday'), *[Td(course_list[x.fri]) for x in ttble]),
        # Tr(Td('Saturday'), *[Td(course_list[x.sat]) for x in ttble]),
        Tr(Td(A("Return", href="/view/timetable/"), colspan=10)),
        id="student_display", name="student_display",

    ))

    return table2

@rt('/view/timetable/edit/')
def put(day:str, time:str, cur_val:str, rowid:int):
    print(day, time, cur_val)
    course_list = [x.name for x in courses()]
    # timetable.update(1, mon=1, tue=2, wed=3, thu=4, fri=5, sat=6)
    cont = Td(get_dropdown(course_list, int(cur_val), day, time, rowid))
    return cont

@rt('/view/timetable/edit/')
def post(t:dict):
    print(t)
    # row = timetable.get(where)
    # collist = [x.name for x in timetable.columns]
    timetable.update(id=t["id"], updates={list(t.keys())[0]:list(t.values())[0]})
    return Meta(http_equiv="refresh", content=f"0;/view/timetable/edit")



serve(port=5252)