from fasthtml.common import *
from nav import get_navbar
def register_timetable(app, rt, db):
    courses = db.t.course
    timetable = db.t.timetable
    Timetable = timetable.dataclass()
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

        collist = [x.name for x in timetable.columns]
        y = 5  # starting index of days in timetable table

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