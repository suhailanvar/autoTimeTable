from fasthtml.common import *
from nav import get_navbar
def register_course(app, rt, db):
    course = db.t.course
    Course = course.dataclass()
    @rt('/view/course/')
    def get(session):
        heading = f"Course List"

        query = f'''
            SELECT
                c.*,
                GROUP_CONCAT(d.short_name, ', ') AS degree_names
            FROM
                course c
            JOIN
                course_degree cp ON c.id = cp.course_id
            JOIN
                degree d ON cp.degree_id = d.id
            GROUP BY
                c.id, c.name;
        '''

        query2 = f'''
            SELECT * FROM course;
        '''

        Style("td{--pico-font-weight: 700;}")

        table = Table(
            Thead(Tr(Th('Id', scope="col"), Th('Code'), Th("Name"), Th("Credits"), Th("Level"), Th("Programme(s)"))),
            *[Tr(Td(x["id"]), Td(x["code"]), Td(x["name"]), Td(x["credits"]), Td(x["level"]), Td(x["degree_names"])) for x in db.q(query)],
            id="student_display", name="student_display", style=""
        )

        # Divide the report further into PE and OE versions
        # query = f'''
        #             select c.name, count(c.name)
        #             from {elected_courses} as e inner join {courses} as c on e.course_id = c.id
        #             group by c.name
        #             order by count(c.name) desc;
        #         '''
        # sub_selection_count = [x for x in db.execute(query)]
        # subject_selection_report = Div(H3("Subject Selection Report"),
        #                                Table(
        #                                    *[Tr(Td(x[0]), Td(x[1])) for x in sub_selection_count],
        #                                ), style="margin:auto; width:50%;")

        page = Titled(heading, table, style='margin:auto; width:70%;')
        return get_navbar(),  page