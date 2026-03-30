from django.test import TestCase
import json

from apps.core.models import Question, Quiz

class QuestionTest(TestCase):
    def setUp(self):
        self.quiz = Quiz.objects.create(title="Sample Quiz", description="A test quiz")
        self.question_data = {
            "title": "What is the capital of France?",
            "answerRight": 0,
            "answerOptions": json.dumps(["Paris", "London", "Rome", "Berlin"]),
            "explanation": "It is Paris",
            "InQuiz": self.quiz
        }
        self.question = Question.objects.create(**self.question_data)

    def test_create_question(self):
        saved_question = Question.objects.get(id=self.question.id)
        self.assertIsNotNone(saved_question)
        self.assertEqual(saved_question.id, self.question.id)
        self.assertEqual(saved_question.title, self.question_data["title"])
        self.assertEqual(saved_question.answerRight, self.question_data["answerRight"])
        self.assertEqual(saved_question.answerOptions, self.question_data["answerOptions"])
        self.assertEqual(saved_question.explanation, self.question_data["explanation"])
        self.assertEqual(saved_question.InQuiz, self.quiz)

    def test_update_question(self):
        new_question_title = "What is the capital of Spain?"
        self.question.title = new_question_title
        self.question.save()

        updated_question = Question.objects.get(id=self.question.id)
        self.assertEqual(updated_question.title, new_question_title)
        self.assertEqual(updated_question.answerRight, self.question_data["answerRight"])

    def test_delete_question(self):
        question_id = self.question.id
        self.question.delete()

        with self.assertRaises(Question.DoesNotExist):
            Question.objects.get(id=question_id)

    def test_str(self):
        expected_str = (
            f"{self.question.title}"
            f" (InQuiz={self.question.InQuiz}, createdAt={self.question.createdAt}, updatedAt={self.question.updatedAt})"
        )
        self.assertEqual(str(self.question), expected_str)

    def test_timestamps(self):
        self.assertIsNotNone(self.question.createdAt)
        self.assertIsNotNone(self.question.updatedAt)
