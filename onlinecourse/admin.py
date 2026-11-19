from django.contrib import admin
# Import the seven model classes
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission


# ChoiceInline: edit choices inside the Question admin page
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 2


# QuestionInline: edit questions inside the Course admin page
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2


# LessonInline: edit lessons inside the Course admin page
class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5


# Course admin
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline, QuestionInline]
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']


# QuestionAdmin: lists questions and lets choices be edited inline
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['question_text', 'course', 'grade']
    list_filter = ['course']
    search_fields = ['question_text']


# LessonAdmin
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
    list_filter = ['course']
    search_fields = ['title', 'content']


# Register models
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
