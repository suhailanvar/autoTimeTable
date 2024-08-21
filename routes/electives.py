from fasthtml.common import *
from nav import get_navbar
def register_electives(app, rt, db):
    courses = db.t.course
    elected_courses = db.t.elected_courses
    Elected_course = elected_courses.dataclass()
    def get_electives_row():
        query1 = f'''
            select s.*, d.name
            from student s inner join degree d on d.id = s.degree_id;
        '''

        student_list = [x for x in db.execute(query1)]

        for student in student_list:
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
                     pe[0] if len(pe) > 0 else Td(""), pe[1] if len(pe) > 1 else Td(""),
                     pe[2] if len(pe) > 2 else Td(""),
                     oe[0] if len(oe) > 0 else Td(""), oe[1] if len(oe) > 1 else Td(""),
                     oe[2] if len(oe) > 2 else Td(""))
            # *pe, *oe)

    @rt('/view/electives/')
    def get(year: str = "2024", sem: str = "3"):
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
        subject_selection_report = Div(H3("Subject Selection Report"),
                                       Table(
                                           *[Tr(Td(x[0]), Td(x[1])) for x in sub_selection_count],
                                       ), style="margin:auto; width:50%;")

        page = Titled(heading, table, style='margin:auto; width:70%;')
        return get_navbar(), page, subject_selection_report