from fasthtml.common import *
from nav import get_navbar
def register_timetable(app, rt, db):
    courses = db.t.course
    timetable = db.t.timetable
    Timetable = timetable.dataclass()
    degree = db.t.degree



    # creates default db values for each degree if it does not exist
    def create_timetable_db_template() :
        degrees = [x["id"] for x in degree()]
        degrees_with_timetables = [x.degree_id for x in timetable(where="year='2024' and sem='3'", select="distinct degree_id")]

        for d in degrees :
            if d not in degrees_with_timetables :
                # insert default timetable values for each degree based on the first degree
                # should update this to be based on a base template
                for t in timetable(where="year='2024' and sem='3' and degree_id=1") :
                    timetable.insert(year="2024", sem="3", degree_id=d, time=t.time)  # day values should default to 0

        print("Hello!",degrees_with_timetables)

    create_timetable_db_template()

    @rt('/view/timetable/')
    def get(session, year:str=None, sem:str=None, deg:str=None):

        print("Inside Get sess",session)
        print("Inside Get2",year, sem, deg)

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

        print("Inside Get3 sess", year, sem, deg)
        print("Inside Get4", year, sem, deg)

        # print(session)

        def get_year_dropdown(year):
            yearlist = [x.year for x in timetable(select="distinct year")]
            # print(yearlist)
            return Select(
                *[Option(x, value=x, selected=(True if x == year else False)) for x in yearlist],
                name="year", id="year",
            )

        def get_sem_dropdown(sem):
            semlist = [x.sem for x in timetable(select="distinct sem")]
            # print(semlist)
            return Form(Select(
                *[Option(f"Semester {x}", value=x, selected=(True if x == sem else False)) for x in semlist],
                name="sem", id="sem"
            ))

        def get_degree_dropdown(deg):
            degreelist = [x for x in degree()]
            # print(degreelist)
            return Form(Select(
                *[Option(x.name, value=x.id, selected=(True if x.id == int(deg) else False)) for x in degreelist],
                name="deg", id="deg", hx_post="/view/timetable/", hx_trigger="change"
            ))

        course_list = [x.name for x in courses()]
        print("View timetable Courselist", course_list)

        query = f'''
                    select * from course
                    inner join course_degree on course.id = course_degree.course_id
                    where course_degree.degree_id = {int(deg)};
                '''

        course_list2 = {x[0]: x[2] for x in db.execute(query)}
        course_list2[0] = "-"

        print("View timetable Courselist22", course_list2)


        heading = H1(f"Timetable", get_year_dropdown(session['year']), get_sem_dropdown(session['sem']), get_degree_dropdown(deg), cls="grid")
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

        time_list = [x.time for x in timetable(where=f"year='{year}' and sem='{sem}' and degree_id={int(deg)}")]
        ttble = timetable(where=f"year='{year}' and sem='{sem}' and degree_id={int(deg)}")

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
            Tr(Td(A("Edit", href="/view/timetable/edit/"), colspan=10)),
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

        page = Div(heading, table2,Br(), style='margin:auto; width:70%;', cls="overflow-auto")
        return get_navbar(), page

    @rt('/view/timetable/')
    def post(session, year:str=None, sem:str=None, deg:str=None):
        print("view",year, sem, deg)
        if year : session['year'] = year
        else : year = session['year']
        if sem : session['sem'] = sem
        else : sem = session['sem']
        if deg : session['degree'] = deg
        else : deg = session['degree']
        print("view2", year, sem, deg)
        print("Inside post", session)
        # session['year'] = year if year else year = session['year']
        # session['sem'] = sem if sem else sem = session['sem']
        # session['degree'] = degree if degree else degree = session['degree']
        return Meta(http_equiv="refresh", content=f"0;/view/timetable/?year={year}&sem={sem}&degree={deg}")

    def get_dropdown(course_list, current_sub_value, day, time, rowid) :

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
            # Option("-", value=0, selected=(True if current_sub_value == "0" else False), name=f"{day}", id=f"{day}"),
            *[Option(course_name, value=course_id, selected=(True if course_name == course_list[current_sub_value] else False)) for course_id, course_name in course_list.items()],
            name=f"{day}", id=f"{day}"
        )

        cont = Form(dropdown,
                    Hidden(name="time", value=time),
                    # Hidden(name="cur_val", value=current_value),
                    # Hidden(name="day", value=day),
                    Hidden(name="id", value=rowid),
                    A("Change", hx_post="/view/timetable/edit/"))
        # print("Course list index", course_list.index("Computer Vision"))

        return cont


    def get_td_template(course_list, collist, deg, ttable_row, day_index, i) :
        cont = Td(course_list[int(ttable_row[collist[day_index+i]])], A("Edit",
                            hx_put=f"/view/timetable/edit/?deg={deg}&day={collist[day_index+i]}&time={ttable_row["time"]}&cur_sub_id={ttable_row[collist[day_index+i]]}&rowid={ttable_row["id"]}",
                                                             hx_target=f"#edit_main-{i}{ttable_row["id"]}", hx_swap="outerHTML"),
                             id=f"edit_main-{i}{ttable_row["id"]}")
        print("Inside get_td_template", course_list, collist, deg, ttable_row, day_index, i, course_list[int(ttable_row[collist[day_index+i]])],
              collist[day_index+i], ttable_row["time"], ttable_row[collist[day_index+i]], ttable_row["id"], "\n")
        return cont

    def get_deg_courselist(deg):
        query = f'''
                            select * from course
                            inner join course_degree on course.id = course_degree.course_id
                            where course_degree.degree_id = {int(deg)}
                        '''

        course_list = {x[0]: x[2] for x in db.execute(query)}
        course_list[0] = "-"

        return course_list

    @rt('/view/timetable/edit/')
    def get(session, year:str=None, sem:str=None, deg:str=None):

        if year : session['year'] = year
        else : year = session['year']
        if sem : session['sem'] = sem
        else : sem = session['sem']
        if deg : session['degree'] = deg
        else : deg = session['degree']

        print("Inside Get edit", year, sem, deg)

        query = f'''
            select * from course
            inner join course_degree on course.id = course_degree.course_id
            where course_degree.degree_id = {int(deg)};
        '''

        course_list = {x[0]:x[2] for x in db.execute(query)}
        course_list[0] = "-"
        print(course_list)
        time_list = [x.time for x in timetable(where=f"year='{year}' and sem='{sem}' and degree_id={int(deg)}")]
        ttble = timetable(where=f"year='{year}' and sem='{sem}' and degree_id={int(deg)}", as_cls=False)

        collist = [x.name for x in timetable.columns]
        day_index = 5  # starting index of days in timetable table

        table2 = Form(Table(
            Tr(Th('Day'), *([Th(time) for time in time_list])),
            *[Tr(Td(day), *[get_td_template(course_list, collist, deg, row, day_index, i) for row in ttble])
              for i, day in enumerate(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])],
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
    def put(deg:str, day:str, time:str, cur_sub_id:str, rowid:int):
        print("Inside Put",day, time, cur_sub_id, rowid)

        course_list = get_deg_courselist(int(deg))
        # timetable.update(1, mon=1, tue=2, wed=3, thu=4, fri=5, sat=6)
        cont = Td(get_dropdown(course_list, int(cur_sub_id), day, time, rowid))
        return cont

    @rt('/view/timetable/edit/')
    def post(t:dict):
        print(t)
        # row = timetable.get(where)
        # collist = [x.name for x in timetable.columns]
        timetable.update(id=t["id"], updates={list(t.keys())[0]:list(t.values())[0]})
        return Meta(http_equiv="refresh", content=f"0;/view/timetable/edit/")