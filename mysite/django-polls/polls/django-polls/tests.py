# -*- coding: utf-8 -*-
import datetime
#from __future__ import unicode_literals
from django.utils import timezone
from django.test import TestCase
from polls.models import Question
from django.core.urlresolvers import reverse

# Create your tests here.
#class QuestionMethodTests(TestCase):
    #def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for questions whose pub_date is in the future
        """
    #    time = timezone.now() + datetime.timedelta(days=30)
    #    future_question = Question(pub_date=time)
    #    self.assertEqual(future_question.was_published_recently(), False)
    #def test_was_published_recently_with_old_question(self):
        """
    #    was_published recently() should return False for question whose pub_date is older than 1 day
        """
    #    time = timezone.now() - datetime.timedelta(days=30)
    #    old_question = Question(pub_date=time)
    #    self.assertEqual(old_question.was_published_recently(),False)
    #def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() should return True for questions whose pub_date is within the last day
        """
     #   time = timezone.now() - datetime.timedelta(hours=1)
     #   recent_question = Question(pub_date=time)
     #   self.assertEqual(recent_question.was_published_recently(), True)

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionViewTests(TestCase):
#class QuestionIndexDetailTests(TestCase):
    def test_index_view_with_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
    #def test_index_view_with_a_past_question(self):
    def test_detail_view_with_a_past_question(self):
        create_question(question_text='Past Question.', days=-30)
        response = self.client.get(reverse('polls:index')) 
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )
    #def test_index_view_with_a_future_question(self):
    def test_detail_view_with_a_future_question(self):
        future_question = create_question(question_text='Future question.', days=5)
        response = self.client.get(reverse('polls:detail', args=(future_question.id,)))
        self.assertEqual(response.status code, 404)
        #create _question(question_text="Future question.", days=30)
        #response = self.client.get(reverse('polls:index'))
        #self.assertContains(response, "No polls are available.",
                            status_code=200)
        #self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_index_view_with_future_question_and_past_question(self):
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_two_past_questions(self):
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', 'Question: Past question 1.>']
        )

