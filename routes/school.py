from fasthtml.common import *
from nav import get_navbar
def register_school(app, rt, db):
    school = db.t.school
    School = school.dataclass()
    @rt('/view/schools/')
    def get(session):
        heading = f"School List"

        query = f'''
            SELECT 
                s.*,
                (select count(*) from degree where school_id = s.id) as degree_count,
                count(distinct cp.course_id) as subject_count,
                count(distinct s2.id) as student_count
            FROM 
                school s
            LEFT JOIN
                degree d ON s.id = d.school_id
            LEFT JOIN
                course_degree cp ON d.id = cp.degree_id
            LEFT JOIN
                student s2 on d.id = s2.degree_id
            GROUP BY
                s.id, s.name;
        '''

        table = Table(
            Tr(Th('Id'), Th('Name'), Th("Full Name"), Th("Description"), Th("Degree Count"), Th("Subject Count"), Th("Student Count")),
            *[Tr(Td(x[0]), Td(x[1]), Td(x[2]), Td(x[3]), Td(x[4]), Td(x[5]), Td(x[6])) for x in db.execute(query)],
            id="student_display", name="student_display",
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
        return get_navbar(), page