from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import Course, Enrollment, Choice, Submission


class ExamFlowTests(TestCase):
    def setUp(self):
        call_command('seed_demo', verbosity=0)
        self.course = Course.objects.get(name='Learning Django')
        self.user = User.objects.get(username='learner')
        self.client.login(username='learner', password='p@ssword123')
        self.client.post(reverse('onlinecourse:enroll', args=(self.course.id,)))

    def _submit(self, choices):
        data = {f'choice_{c.id}': c.id for c in choices}
        return self.client.post(reverse('onlinecourse:submit', args=(self.course.id,)), data)

    def test_enroll_creates_enrollment(self):
        self.assertTrue(Enrollment.objects.filter(user=self.user, course=self.course).exists())

    def test_all_correct_passes(self):
        correct = Choice.objects.filter(question__course=self.course, is_correct=True)
        response = self._submit(correct)
        submission = Submission.objects.latest('id')
        self.assertRedirects(response, reverse('onlinecourse:exam_result',
                                               args=(self.course.id, submission.id)))
        page = self.client.get(response.url)
        self.assertEqual(page.context['grade'], 100)
        self.assertContains(page, 'Congratulations')

    def test_wrong_choice_loses_question_score(self):
        chosen = list(Choice.objects.filter(question__course=self.course, is_correct=True))
        chosen.append(Choice.objects.filter(question__course=self.course, is_correct=False).first())
        response = self._submit(chosen)
        page = self.client.get(response.url)
        self.assertEqual(page.context['grade'], 50)
        self.assertContains(page, 'Failed')
