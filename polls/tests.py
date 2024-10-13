from django.test import TestCase
from django.urls import reverse
from .models import Question, Choice
from django.utils import timezone


class PollsViewsTestCase(TestCase):
    def setUp(self):
        # Create a sample question and choice for testing
        self.question = Question.objects.create(
            question_text="Sample Question", pub_date=timezone.now()
        )
        self.choice = Choice.objects.create(
            question=self.question, choice_text="Sample Choice", votes=0
        )

    def test_index_view(self):
        # Test the index view
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sample Question")
        self.assertEqual(
            list(response.context["latest_question_list"]), [self.question]
        )

    def test_detail_view(self):
        # Test the detail view with a valid question
        response = self.client.get(reverse("polls:detail", args=(self.question.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sample Question")

    def test_results_view(self):
        # Test the results view with a valid question
        response = self.client.get(reverse("polls:results", args=(self.question.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sample Question")

    def test_vote_view_with_valid_choice(self):
        # Test voting with a valid choice
        response = self.client.post(
            reverse("polls:vote", args=(self.question.id,)), {"choice": self.choice.id}
        )
        self.assertEqual(response.status_code, 302)  # Should redirect to results
        self.choice.refresh_from_db()
        self.assertEqual(self.choice.votes, 1)

    def test_vote_view_without_choice(self):
        # Test voting without selecting a choice
        response = self.client.post(reverse("polls:vote", args=(self.question.id,)), {})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You didn&#x27;t select a choice.")
