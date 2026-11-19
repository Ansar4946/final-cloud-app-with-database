# Online Course App with Assessment Feature

A Django online-course application extended with an exam (assessment) feature:
learners enroll in a course, take a multiple-choice exam and see their graded result.

## What's included

| Part | File |
| --- | --- |
| `Question`, `Choice` and `Submission` models | [onlinecourse/models.py](onlinecourse/models.py) |
| Admin: `QuestionInline`, `ChoiceInline`, `QuestionAdmin`, `LessonAdmin` | [onlinecourse/admin.py](onlinecourse/admin.py) |
| Course detail page with lessons and the exam form | [onlinecourse/templates/onlinecourse/course_details_bootstrap.html](onlinecourse/templates/onlinecourse/course_details_bootstrap.html) |
| `submit` and `show_exam_result` views | [onlinecourse/views.py](onlinecourse/views.py) |
| Routes for `submit` and `show_exam_result` | [onlinecourse/urls.py](onlinecourse/urls.py) |
| Exam result page | [onlinecourse/templates/onlinecourse/exam_result_bootstrap.html](onlinecourse/templates/onlinecourse/exam_result_bootstrap.html) |
| Screenshots | [screenshots/](screenshots/) |

## Grading rule

Each question carries a grade (points). A question earns its points only when the learner
selects every correct choice and no incorrect one. The final grade is the percentage of
points earned; a grade above 80 passes.

## Run locally

```bash
python -m venv .venv
.venv/Scripts/activate        # Windows (use: source .venv/bin/activate on macOS/Linux)
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo    # demo admin, learner, course, lessons and questions
python manage.py runserver
```

Open http://127.0.0.1:8000/onlinecourse/ and the admin site at http://127.0.0.1:8000/admin/.
The demo accounts are `admin` and `learner`, both with password `p@ssword123` (local use only).

Run the tests with `python manage.py test onlinecourse`.
