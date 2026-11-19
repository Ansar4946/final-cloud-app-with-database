from datetime import date

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from onlinecourse.models import Course, Lesson, Instructor, Question, Choice


class Command(BaseCommand):
    help = "Create a demo superuser, learner, course, lessons and exam questions."

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'p@ssword123', first_name='Admin')
        if not User.objects.filter(username='learner').exists():
            User.objects.create_user('learner', password='p@ssword123', first_name='Alex', last_name='Learner')

        admin_user = User.objects.get(username='admin')
        instructor, _ = Instructor.objects.get_or_create(user=admin_user, defaults={'total_learners': 0})

        course, created = Course.objects.get_or_create(
            name='Learning Django',
            defaults={
                'description': 'Build full-stack web apps with the Django framework.',
                'pub_date': date(2026, 1, 15),
            },
        )
        if not created:
            self.stdout.write('Demo course already exists; nothing to do.')
            return
        course.instructors.add(instructor)

        lessons = [
            ('Introduction to Django', 'Django is a high-level Python web framework that encourages rapid development.'),
            ('Models and the ORM', 'Models describe your data; the ORM maps them to database tables.'),
            ('Views and Templates', 'Views handle requests and templates render HTML responses.'),
        ]
        for order, (title, content) in enumerate(lessons):
            Lesson.objects.create(course=course, order=order, title=title, content=content)

        questions = [
            ('Which command creates a new Django app?', 50, [
                ('python manage.py startapp', True),
                ('python manage.py runserver', False),
                ('django-admin newapp', False),
            ]),
            ('Which of these are Django model field types?', 50, [
                ('CharField', True),
                ('ForeignKey', True),
                ('TextBlock', False),
            ]),
        ]
        for text, grade, choices in questions:
            q = Question.objects.create(course=course, question_text=text, grade=grade)
            for choice_text, is_correct in choices:
                Choice.objects.create(question=q, choice_text=choice_text, is_correct=is_correct)

        self.stdout.write(self.style.SUCCESS('Demo data created.'))
