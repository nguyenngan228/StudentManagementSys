from datetime import datetime, timedelta

from faker import Faker
from sqlalchemy import Column, String, Integer, Enum, ForeignKey, UniqueConstraint, Float, DATE
from manageapp import db, app
from flask_login import UserMixin
from enum import Enum as MyEnum
from sqlalchemy.orm import relationship



class Grade(MyEnum):
    G10 = 1
    G11 = 2
    G12 = 3


class UserRole(MyEnum):
    EMPLOYEE = 1
    TEACHER = 2
    ADMIN = 3


class Sex(MyEnum):
    FEMALE = 1
    MALE = 2
    ANOTHER = 3


class Semester(MyEnum):
    S1 = 1
    S2 = 2


class User(db.Model, UserMixin):
    id = Column(Integer, autoincrement=True, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    user_role = Column(Enum(UserRole), nullable=False)
    my_classes = relationship('MyClass', backref='user', lazy=True)


class Student(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    dob = Column(DATE, nullable=False)
    address = Column(String(100))
    sex = Column(Enum(Sex))
    phone = Column(String(100), unique=True)
    email = Column(String(100), unique=True)
    studyings = relationship('Studying', backref='student', lazy=True)




class MyClassDetail(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    my_classes = relationship('MyClass', backref='my_class_detail', lazy=True)


class MyClass(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    my_class_detail_id = Column(Integer, ForeignKey(MyClassDetail.id), nullable=False)
    school_year_id = Column(Integer, ForeignKey('school_year.id'), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    studyings = relationship('Studying', backref='my_class', lazy=True)
    outlines = relationship('Outline', backref='my_class', lazy=True)

    __table_args__ = (
        UniqueConstraint('my_class_detail_id', 'school_year_id', name='uq_class_year'),
        UniqueConstraint('user_id', 'school_year_id', name='uq_user_year') #giao vien co the chu nhiem nhieu lop nhung 1 nam chi chu nhiem 1 lop
    )



class Studying(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    student_id = Column(Integer, ForeignKey(Student.id), nullable=False)
    my_class_id = Column(Integer, ForeignKey(MyClass.id), nullable=False)
    scores = relationship('Score', backref='studying', lazy=True)



class SchoolYear(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    year = Column(String(50), nullable=False, unique=True)
    my_classes = relationship(MyClass, backref='school_year', lazy=True)


class Score(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    studying_id = Column(Integer, ForeignKey(Studying.id), nullable=False)
    subject_id = Column(Integer, ForeignKey('subject.id'), nullable=False)
    type_id = Column(Integer, ForeignKey('score_type.id'), nullable=False)
    semester = Column(Enum(Semester), nullable=False)
    value = Column(Float, nullable=False)


class ScoreType(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    scores = relationship(Score, backref='score_type', lazy=True)
    outlines = relationship('Outline', backref='score_type', lazy=True)


class Subject(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), nullable=False)
    grade = Column(Enum(Grade))
    scores = relationship(Score, backref='subject', lazy=True)
    outlines = relationship('Outline', backref='subject', lazy=True)

    __table_args__ = (
        UniqueConstraint('name', 'grade', name='uq_name_grade'),
    )


class Outline(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    subject_id = Column(Integer, ForeignKey(Subject.id), nullable=False)
    my_class_id = Column(Integer, ForeignKey(MyClass.id), nullable=False)
    score_type_id = Column(Integer, ForeignKey(ScoreType.id), nullable=False)
    number_score = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint('subject_id', 'my_class_id', 'score_type_id', name='uq_subject_class_score_type'),
    )



class Rule(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), nullable=False)
    value = Column(Integer, nullable=False)
#




if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # students = db.session.query(Studying.id.label('studying_id'), Student.id, Student.first_name, Student.last_name) \
        #     .join(Studying, Studying.student_id == Student.id) \
        #     .filter(Studying.my_class_id == 21).all()
        # print(students)
        #
        # query = text("""
        #        WITH subAllScores AS (
        #      SELECT
        #          s.id,
        #          s.first_name,
        #          s.last_name,
        #          score_type.name as type,
        #          sc.value
        #      FROM
        #          student s
        #      JOIN
        #          studying st ON s.id = st.student_id
        #      JOIN
        #          score sc ON sc.studying_id = st.id
        #      JOIN
        #          score_type ON sc.type_id = score_type.id
        #      WHERE
        #          sc.subject_id = :subject_id
        #          AND st.my_class_id = :my_class_id
        #          AND sc.semester= :semester
        #  ),
        #  dao_score AS (
        #      SELECT
        #          id
        #          first_name,
        #          last_name,
        #          GROUP_CONCAT(CASE WHEN type = '15 phút' THEN value ELSE NULL END ORDER BY value) AS fifteen_minutes,
        #          GROUP_CONCAT(CASE WHEN type = '1 tiết' THEN value ELSE NULL END ORDER BY value) AS one_hour,
        #          GROUP_CONCAT(CASE WHEN type = 'Thi cuối kì' THEN value ELSE NULL END ORDER BY value) AS final_test
        #      FROM
        #          subAllScores
        #      GROUP BY
        #          id, first_name, last_name
        #  )
        #
        #  SELECT * FROM dao_score;
        #  """)
        #
        # se = Semester(1).name
        # # Truyền giá trị tham số vào khi thực thi truy vấn
        # result = db.session.execute(query, {"subject_id": 2, "my_class_id": 21,
        #                                     "semester": 'S1'})
        #
        # # Lấy kết quả
        # scores_results = []
        # for row in result:
        #     scores_results.append(row)
        # print(scores_results)
        # db.create_all()

        # student = Student(first_name="NV", last_name="A", dob='2009-09-09',
        #                            address="HCM", sex=Sex.FEMALE, phone='093729833', email='nvb@gmail.com')
        # db.session.add(student)
        # db.session.commit()
        #
        # import hashlib
        #
        #
        #
        # u1 = User(first_name='Hong',
        #          last_name='Hae In',
        #          username='teacher1',
        #          password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #          user_role = UserRole.TEACHER)
        #
        # u2 = User(first_name='Lee',
        #          last_name='Jong Suk',
        #          username='teacher2',
        #          password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #          user_role=UserRole.TEACHER)
        # u3 = User(first_name='Ngo',
        #           last_name='Thanh Van',
        #           username='teacher3',
        #           password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #           user_role=UserRole.TEACHER)
        # u4 = User(first_name='Nhi',
        #           last_name='Nhi',
        #           username='teacher4',
        #           password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #           user_role=UserRole.TEACHER)
        # u5 = User(first_name='Minh',
        #           last_name='Anh',
        #           username='teacher5',
        #           password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #           user_role=UserRole.TEACHER)
        # u6 = User(first_name='Gia',
        #           last_name='An',
        #           username='teacher6',
        #           password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #           user_role=UserRole.TEACHER)
        #
        # u7 = User(first_name='Ngoc',
        #           last_name='Lan',
        #           username='teacher7',
        #           password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #           user_role=UserRole.TEACHER)
        #
        # u8 = User(first_name='Phi',
        #           last_name='Nhung',
        #           username='teacher8',
        #           password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #           user_role=UserRole.TEACHER)
        #
        # u9 = User(first_name='My',
        #           last_name='Linh',
        #           username='teacher9',
        #           password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #           user_role=UserRole.TEACHER)
        #
        # u10 = User(first_name='Nguyen',
        #           last_name='Van Anh',
        #           username='admin',
        #           password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #           user_role = UserRole.ADMIN)
        # u11 = User(first_name='Nguyen',
        #           last_name='Thi Van',
        #           username='employee1',
        #           password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #           user_role=UserRole.EMPLOYEE)
        # u12 = User(first_name='Nguyen',
        #           last_name='Ngan',
        #           username='nn83',
        #           password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()),
        #           user_role=UserRole.ADMIN)
        #
        # db.session.add_all([u1,u2,u3,u4,u5,u6,u7,u8,u9,u10,u11,u12])
        # db.session.commit()
        # import hashlib
        #


        # db.session.add_all([u7,u8,u9])
        # db.session.commit()
        # mclass = MyClass.query.get(1)
        # print(mclass.my_class_detail.name)

        # classrooms = db.session.query(MyClassDetail.name, MyClass.id) \
        #     .join(MyClass, MyClass.my_class_detail_id == MyClassDetail.id) \
        #     .join(Studying, Studying.my_class_id == MyClass.id) \
        #     .filter(MyClass.school_year_id == app.config["YEAR"], MyClassDetail.id != 1,
        #             MyClassDetail.name.icontains('10A1'[:2])) \
        #     .group_by(MyClass.id) \
        #     .having(func.count(Studying.student_id) < 5) \
        #     .all()
        # print(classrooms)

        fake = Faker('vi_VN')
        # Tạo 1000 đối tượng Student giả lập

        # Tạo set để lưu trữ các email và số điện thoại đã được tạo
        unique_emails = set()
        unique_phones = set()

        # Tính toán ngày sinh cho đối tượng Student trong khoảng từ 15 đến 20 tuổi
        start_date = datetime.now() - timedelta(days=20 * 365)
        end_date = datetime.now() - timedelta(days=15 * 365)

        # Tạo 1000 đối tượng Student giả lập
        while len(unique_emails) < 45: #12+15+9+9
            first_name = fake.first_name()
            last_name = fake.last_name()
            dob = fake.date_of_birth(minimum_age=15, maximum_age=20)
            address = fake.address()
            sex = fake.random_element(elements=(Sex.FEMALE, Sex.MALE, Sex.ANOTHER))

            phone = fake.phone_number()
            email = fake.email()

            # Kiểm tra tính duy nhất của email và số điện thoại
            if email not in unique_emails and phone not in unique_phones:
                unique_emails.add(email)
                unique_phones.add(phone)

                # Tạo đối tượng Student và thêm vào session
                student = Student(first_name=first_name, last_name=last_name, dob=dob,
                                  address=address, sex=sex, phone=phone, email=email)
                db.session.add(student)

        # Commit các thay đổi vào cơ sở dữ liệu
        db.session.commit()
