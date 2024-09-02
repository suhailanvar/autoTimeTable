from fasthtml.common import *
from nav import get_navbar
def register_electives(app, rt, db):
    courses = db.t.course
    elected_courses = db.t.elected_courses
    Elected_course = elected_courses.dataclass()
    degree = db.t.degree
    Degree = degree.dataclass()
    def get_electives_row(option, edit=False):

        print("Option", option, type(option))

        query1 = f'''
            select s.*, d.name
            from student s inner join degree d on d.id = s.degree_id;
        '''
        if int(option) != 0:
            query1 = f'''
                select s.*, d.name deg
                from student s inner join degree d on d.id = s.degree_id
                where degree_id = {option};
            '''

        student_list = [x for x in db.q(query1)]
        print(student_list)

        for student in student_list:
            # elective_list = [x for x in db.execute(query2.replace('1', str(student[0])))]
            query2 = f'''
                    select e.student_id, e.course_type, e.course_id, c.name
                   from {elected_courses} as e inner join {courses} as c on e.course_id = c.id
                    where e.student_id = {student["id"]}
                    order by e.course_type desc, c.name;
                '''
            elective_list = [x for x in db.q(query2)]
            pe = [x["name"] for x in elective_list if x["course_type"] == 'PE']
            oe = [x["name"] for x in elective_list if x["course_type"] == 'OE']
            # print(elective_list)
            yield Tr(Td(student["id"]), Td(student["name"]), Td(student["deg"]),
                     Td(pe[0]) if len(pe) > 0 else Td(""), Td(pe[1]) if len(pe) > 1 else Td(""),
                     Td(pe[2]) if len(pe) > 2 else Td(""),
                     Td(oe[0]) if len(oe) > 0 else Td(""), Td(oe[1]) if len(oe) > 1 else Td(""),
                     Td(oe[2]) if len(oe) > 2 else Td(""),
                     # Td(A("Edit", hx_put=f"/electives/edit/?year={2024}&sem{3}&deg={option}&stud_id={student["id"]}")) if edit else "",
                     Td(A("Edit2",
                          hx_put=f"/electives/edit2/?e={Elected_course()}")) if edit else "",
                     id=f"student-{student['id']}", name=f"student-{student['id']}")
            # *pe, *oe)

    @rt('/electives/view/')
    def get(session, year:str=None, sem:str=None, deg:str=None):

        if not session['year'] :
            if year : session['year'] = year
            else : session['year'] = "2024"
        else : year = session['year']

        if not session['sem'] :
            if sem : session['sem'] = sem
            else : session['sem'] = "3"
        else : sem = session['sem']

        if not session['degree'] :
            if deg : session['degree'] = deg
            else : session['degree'] = 1
        else : deg = session['degree']
        def get_degree_dropdown(deg):
            degreelist = [x for x in degree()]
            degreelist.insert(0, Degree(id=0, name="All"))
            # print(degreelist)
            return Form(Select(
                *[Option(x.name, value=x.id, selected=(True if x.id == int(deg) else False)) for x in degreelist],
                name="deg", id="deg", hx_post="/electives/view/", hx_trigger="change"
            ))

        heading = H1(f"Elective List | {year} | Semester {sem}", get_degree_dropdown(deg), cls="grid")

        table = Table(
            Tr(Th('Roll No.'), Th('Name'), Th("Degree"), Th("PE1"), Th("PE2"), Th("PE3")
               , Th("OE1"), Th("OE2"), Th("OE3")),
            *[x for x in get_electives_row(option=deg)],
            Tr(Td(A("Edit", href=f"/electives/edit/?year={year}&sem{sem}=&deg={deg}"), colspan=9)),
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
        subject_selection_report = Div(H3("Subject Selection Report"),
                                       Table(
                                           *[Tr(Td(x[0]), Td(x[1])) for x in sub_selection_count],
                                       ), style="margin:auto; width:50%;")

        page = Div(heading, table, style='margin:auto; width:70%;')
        return get_navbar(), page, subject_selection_report

    @rt('/electives/view/')
    def post(session, year: str = None, sem: str = None, deg: str = None):
        print("view 123", year, sem, deg)
        if year:
            session['year'] = year
        else:
            year = session['year']
        if sem:
            session['sem'] = sem
        else:
            sem = session['sem']
        if deg:
            session['degree'] = deg
        else:
            deg = session['degree']
        # print("view2", year, sem, deg)
        # print("Inside post", session)
        # session['year'] = year if year else year = session['year']
        # session['sem'] = sem if sem else sem = session['sem']
        # session['degree'] = degree if degree else degree = session['degree']
        return Meta(http_equiv="refresh", content=f"0;/electives/view/?year={year}&sem={sem}&degree={deg}")

    @rt('/electives/edit/')
    def get(session, year: str = None, sem: str = None, deg: str = None):

        if not session['year']:
            if year: session['year'] = year
            else: session['year'] = "2024"  # should get current year using datetime
        elif not year : year = session['year']

        if not session['sem']:
            if sem: session['sem'] = sem
            else: session['sem'] = "3"  # maybe get latest sem from db
        elif not sem : sem = session['sem']

        if not session['degree']:
            if deg: session['degree'] = deg
            else: session['degree'] = 1  # maybe get last degree from db
        elif not deg : deg = session['degree']

        def get_edit_td(course_list, collist, deg, ttable_row, day_index, i):
            cont = Td(course_list[int(ttable_row[collist[day_index + i]])], A("Edit",
                                                                              hx_put=f"/view/timetable/edit/?deg={deg}&day={collist[day_index + i]}&time={ttable_row["time"]}&cur_sub_id={ttable_row[collist[day_index + i]]}&rowid={ttable_row["id"]}",
                                                                              hx_target=f"#edit_main-{i}{ttable_row["id"]}",
                                                                              hx_swap="outerHTML"),
                      id=f"edit_main-{i}{ttable_row["id"]}")
            print("Inside get_td_template", course_list, collist, deg, ttable_row, day_index, i,
                  course_list[int(ttable_row[collist[day_index + i]])],
                  collist[day_index + i], ttable_row["time"], ttable_row[collist[day_index + i]], ttable_row["id"],
                  "\n")
            return cont

        # print("Inside Get edit", year, sem, deg)

        heading = H1(f"Edit Elective List | {year} | Semester {sem}", cls="grid")

        table = Table(
            Tr(Th('Roll No.'), Th('Name'), Th("Degree"), Th("PE1"), Th("PE2"), Th("PE3")
               , Th("OE1"), Th("OE2"), Th("OE3"), Th("Edit")),
            *[x for x in get_electives_row(option=deg, edit=True)],
            Tr(Td(A("Return", href="/electives/view/"), colspan=10)),
            id="elective_display", name="elective_display",
        )

        table2 = Form(Table(
            # Tr(Th('Day'), *([Th(time) for time in time_list])),
            # *[Tr(Td(day), *[get_edit_td(course_list, collist, deg, row, day_index, i) for row in ttble])
            #   for i, day in enumerate(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])],
            # Tr(Td('Monday'), *[Td(x[collist[5]]) for x in ttble]),
            # Tr(Td('Tuesday'), *[Td(course_list[x.tue]) for x in ttble]),
            # Tr(Td('Wednesday'), *[Td(course_list[x.wed]) for x in ttble]),
            # Tr(Td('Thursday'), *[Td(course_list[x.thu]) for x in ttble]),
            # Tr(Td('Friday'), *[Td(course_list[x.fri]) for x in ttble]),
            # Tr(Td('Saturday'), *[Td(course_list[x.sat]) for x in ttble]),
            Tr(Td(A("Return", href="/view/timetable/"), colspan=10)),
            id="student_display", name="student_display",

        ))

        return table

    @rt('/electives/edit/')
    def put(year: int, sem: int, deg: int, stud_id: int, sub_type: str):
        # print("Inside Put", day, time, cur_sub_id, rowid)

        row = Tr()

        course_list = get_deg_courselist(int(deg))
        cont = Td(get_dropdown(course_list, int(cur_sub_id), day, time, rowid))
        # return cont
        return

    @rt('/electives/edit/')
    def post(t: dict):
        print(t)
        # row = timetable.get(where)
        # collist = [x.name for x in timetable.columns]
        timetable.update(id=t["id"], updates={list(t.keys())[0]: list(t.values())[0]})
        return Meta(http_equiv="refresh", content=f"0;/view/timetable/edit/")

    @rt('/electives/edit2/')
    def put(e: Elected_course):
        print("Inside Put2", e)
        #
        # row = Tr()
        #
        # course_list = get_deg_courselist(int(deg))
        # cont = Td(get_dropdown(course_list, int(cur_sub_id), day, time, rowid))
        # return cont
        return e