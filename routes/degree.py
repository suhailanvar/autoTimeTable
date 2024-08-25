from fasthtml.common import *
from nav import get_navbar
def register_degree(app, rt, db):
    degree = db.t.degree
    Degree = degree.dataclass()
    @rt('/view/degrees/')
    def get(session):
        heading = f"Degree List"

        query = f'''
            SELECT 
                d.id, d.name degree, s.name school,
                count(distinct cp.course_id) as course_count,
                count(distinct s2.id) as student_count
            FROM school s
            LEFT JOIN degree d ON s.id = d.school_id
            LEFT JOIN course_degree cp ON d.id = cp.degree_id
            LEFT JOIN student s2 on d.id = s2.degree_id
            GROUP BY d.id, d.name
            ORDER BY s.id;
        '''

        Style("td{--pico-font-weight: 700;}")

        table = Table(
            Thead(Tr(Th('Id', scope="col"), Th('Name'), Th("School"), Th("Course Count"), Th("Student Count"))),
            *[Tr(Td(x["id"]), Td(x["degree"]), Td(x["school"]), Td(x["course_count"]), Td(x["student_count"])) for x in db.q(query)],
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