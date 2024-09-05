from fasthtml.common import *
from nav import get_navbar
import json
def register_electives(app, rt, db):
    courses = db.t.course
    elected_courses = db.t.elected_courses
    Elected_course = elected_courses.dataclass()
    degree = db.t.degree
    Degree = degree.dataclass()
    def get_electives_row(deg, edit=False):

        # print("Option", option, type(option))

        query1 = f'''
            select s.*, d.name
            from student s inner join degree d on d.id = s.degree_id;
        '''
        if int(deg) != 0:
            query1 = f'''
                select s.*, d.name deg
                from student s inner join degree d on d.id = s.degree_id
                where degree_id = {deg};
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

            if len(pe) < 3: pe += ["-"] * (3 - len(pe))
            if len(oe) < 3: oe += ["-"] * (3 - len(oe))

            row_info = dict(stud_id=student["id"], stud_name=student["name"], deg_id=deg, deg_name=student["deg"], pe=pe, oe=oe)
            print("Row Info", row_info)

            # Hidden(name="row_info", value=row_info)
            json_string = json.dumps(row_info)
            print(json_string)

            print("Elective List", pe, oe)
            # print(elective_list)
            yield Form(Tr(Td(student["id"]), Td(student["name"]), Td(student["deg"]),
                     Td(pe[0]), Td(pe[1]), Td(pe[2]), Td(oe[0]), Td(oe[1]), Td(oe[2]),
                     # Td(A("Edit", hx_put=f"/electives/edit/?year={2024}&sem{3}&deg={option}&stud_id={student["id"]}")) if edit else "",
                          Input(type="hidden", name="row_info", value="2"),
                     Td(A("Edit2",
                          hx_put=f"/electives/edit2/", hx_vals=f'{{"myVal": {json_string}}}',
                          hx_target=f"#student-{student['id']}")) if edit else "", hx_swap="outerHTML",
                     id=f"student-{student['id']}", name=f"student-{student['id']}"))
            # *pe, *oe)

    @rt('/electives/view/')
    def get(year:str=None, sem:str=None, deg:str=None):

        # if not session['year'] :
        #     if year : session['year'] = year
        #     else : session['year'] = "2024"
        # else : year = session['year']
        #
        # if not session['sem'] :
        #     if sem : session['sem'] = sem
        #     else : session['sem'] = "3"
        # else : sem = session['sem']
        #
        # if not session['degree'] :
        #     if deg : session['degree'] = deg
        #     else : session['degree'] = 1
        # else : deg = session['degree']

        if not year : year = "2024"  # get this data using datetime
        if not sem : sem = "3"
        if not deg : deg = "2"

        # consider creating a dictionary to contain year, sem and degree
        # this would allow for easy access and manipulation of these values
        def get_degree_dropdown(local_deg):
            degreelist = [x for x in degree()]
            degreelist.insert(0, Degree(id=0, name="All"))
            # print(degreelist)
            return Form(Select(
                *[Option(x.name, value=x.id, selected=(True if x.id == int(local_deg) else False)) for x in degreelist],
                name="deg", id="deg", hx_post=f"/electives/view/{year}-{sem}-{local_deg}", hx_trigger="change"
            ))

        heading = H1(f"Elective List | {year} | Semester {sem}", get_degree_dropdown(deg), cls="grid")

        table = Table(
            Tr(Th('Roll No.'), Th('Name'), Th("Degree"), Th("PE1"), Th("PE2"), Th("PE3")
               , Th("OE1"), Th("OE2"), Th("OE3")),
            *[x for x in get_electives_row(deg=deg)],
            Tr(Td(A("Edit", href=f"/electives/edit/?year={year}&sem={sem}&deg={deg}"), colspan=9)),
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

    @rt('/electives/view/{year}-{sem}-{local_deg}')
    def post(year: str = None, sem: str = None, deg: str = None):
        print("view 123", year, sem, deg)
        # print("view2", year, sem, deg)
        # print("Inside post", session)
        # session['year'] = year if year else year = session['year']
        # session['sem'] = sem if sem else sem = session['sem']
        # session['degree'] = degree if degree else degree = session['degree']
        return Meta(http_equiv="refresh", content=f"0;/electives/view/?year={year}&sem={sem}&deg={deg}")

    @rt('/electives/edit/')
    def get(year: str = None, sem: str = None, deg: str = None):

        #  Write redirect mechanic to redirecct to view page if this page is directly accessed from url

        def get_edit_td(course_list, collist, deg, ttable_row, day_index, i):
            cont = Td(course_list[int(ttable_row[collist[day_index + i]])], A("Edit",
                                                                              hx_put=f"/view/timetable/edit/?year={year}&sem={sem}&deg={deg}&day={collist[day_index + i]}&time={ttable_row["time"]}&cur_sub_id={ttable_row[collist[day_index + i]]}&rowid={ttable_row["id"]}",
                                                                              hx_target=f"#edit_main-{i}{ttable_row["id"]}",
                                                                              hx_swap="outerHTML"),
                      id=f"edit_main-{i}{ttable_row["id"]}")
            print("Inside get_td_template", course_list, collist, deg, ttable_row, day_index, i,
                  course_list[int(ttable_row[collist[day_index + i]])],
                  collist[day_index + i], ttable_row["time"], ttable_row[collist[day_index + i]], ttable_row["id"],
                  "\n")
            return cont

        print("Inside Get edit", year, sem, deg)

        heading = H1(f"Edit Elective List | {year} | Semester {sem}", cls="grid")

        table = Table(
            Tr(Th('Roll No.'), Th('Name'), Th("Degree"), Th("PE1"), Th("PE2"), Th("PE3")
               , Th("OE1"), Th("OE2"), Th("OE3"), Th("Edit")),
            *[x for x in get_electives_row(deg=deg, edit=True)],
            Tr(Td(A("Return", href=f"/electives/view/?year={year}&sem={sem}&deg={deg}"), colspan=10)),
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
    def put(row_info: dict):

        row_info = json.loads(row_info["myVal"])
        print(row_info)

        def get_deg_courselist(deg=None):
            query = f'''
                                select * from course
                                inner join course_degree on course.id = course_degree.course_id '''

            query_deg = f''' where course_degree.degree_id = {deg} ''' if deg else ";"

            course_list = {x["id"]: x["name"] for x in db.q(query+query_deg)}
            course_list[0] = "-"
            # course_list = {x.id:x.name for x in courses()}

            return course_list

        def get_dropdown(course_list, current_sub_value, day="mon",):

            dropdown = Select(
                # Option("-", value=0, selected=(True if current_sub_value == "0" else False), name=f"{day}", id=f"{day}"),
                *[Option(course_name, value=course_id,
                         selected=(True if course_name == current_sub_value else False)) for
                  course_id, course_name in course_list.items()],
                name=f"{day}", id=f"{day}"
            )

            cont = Form(dropdown)

            print("Inside get_dropdown", course_list, current_sub_value, day)

            return cont

        row = Tr(Td(row_info["stud_id"]), Td(row_info["stud_name"]), Td(row_info["deg_name"]),
                     Td(get_dropdown(get_deg_courselist(row_info["deg_id"]), row_info["pe"][0])),
                     Td(get_dropdown(get_deg_courselist(row_info["deg_id"]), row_info["pe"][1])),
                     Td(get_dropdown(get_deg_courselist(row_info["deg_id"]), row_info["pe"][2])),
                     Td(get_dropdown(get_deg_courselist(), row_info["oe"][0])),
                     Td(get_dropdown(get_deg_courselist(), row_info["oe"][1])),
                     Td(get_dropdown(get_deg_courselist(), row_info["oe"][2])),
                     # Td(A("Edit", hx_put=f"/electives/edit/?year={2024}&sem{3}&deg={option}&stud_id={student["id"]}")) if edit else "",
                     Td(A("Change",
                          hx_put=f"/electives/edit2/?e={Elected_course()}", hx_target=f"student-{row_info["stud_id"]}")),
                     id=f"student-{row_info["stud_id"]}", name=f"student-{row_info["stud_id"]}")
        # # #
        # course_list = get_deg_courselist(int(deg))
        # cont = Td(get_dropdown(course_list, int(cur_sub_id), day, time, rowid))
        # return cont
        return row