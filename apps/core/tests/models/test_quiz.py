from django.test import TestCase

from apps.core.models import Creator, Question, Quiz


class QuizModelTest(TestCase):
    def setUp(self):
        self.owner = Creator.objects.create(email="owner@example.com")
        self.question = Question.objects.create(
            title="What is 2 + 2?",
            answerRight=4,
            answerOptions='["1", "2", "3", "4"]',
            explanation="Simple arithmetic.",
        )
        self.quiz = Quiz.objects.create(
            title="Sample Quiz",
            description="This is a sample quiz for testing.",
        )

    def test_create_quiz_defaults(self):
        saved_quiz = Quiz.objects.get(id=self.quiz.id)
        self.assertEqual(saved_quiz.title, "Sample Quiz")
        self.assertEqual(saved_quiz.description, "This is a sample quiz for testing.")
        self.assertEqual(saved_quiz.maxSeconds, 0)
        self.assertEqual(saved_quiz.maxSecondsPerQuestion, 0)
        self.assertEqual(saved_quiz.owner.count(), 0)
        self.assertEqual(saved_quiz.questions.count(), 0)

    def test_add_owner_and_question(self):
        self.quiz.owner.add(self.owner)
        self.quiz.questions.add(self.question)

        refreshed_quiz = Quiz.objects.get(id=self.quiz.id)
        self.assertEqual(refreshed_quiz.owner.count(), 1)
        self.assertEqual(refreshed_quiz.questions.count(), 1)
        self.assertEqual(refreshed_quiz.owner.first(), self.owner)
        self.assertEqual(refreshed_quiz.questions.first(), self.question)

    def test_update_quiz(self):
        new_title = "Updated Quiz Title"
        self.quiz.title = new_title
        self.quiz.save()

        updated_quiz = Quiz.objects.get(id=self.quiz.id)
        self.assertEqual(updated_quiz.title, new_title)
        self.assertEqual(updated_quiz.description, "This is a sample quiz for testing.")

    def test_delete_quiz(self):
        quiz_id = self.quiz.id
        self.quiz.delete()

        with self.assertRaises(Quiz.DoesNotExist):
            Quiz.objects.get(id=quiz_id)

    def test_str_returns_title(self):
        self.assertEqual(str(self.quiz), "Sample Quiz")

    def test_timestamps_are_set(self):
        self.assertIsNotNone(self.quiz.createdAt)
        self.assertIsNotNone(self.quiz.updatedAt)
        self.assertGreaterEqual(self.quiz.updatedAt, self.quiz.createdAt)
