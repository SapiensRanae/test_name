from django.test import TestCase

from apps.core.models import Question

class QuestionTest(TestCase):
    def setUp(self):
        self.question_data = {
            "title": "What is the capital of France?",
            "answerRight": 0,
            "options": ["Paris", "London", "Rome", "Berlin"],
            "explanation": "It is Paris",
            "InQuiz": 2,
        }
        self.question = Question.objects.create(**self.question_data)

    def test_create_question(self):
        saved_question = Question.objects.get(id=self.question.id)
        self.assertIsNotNone(saved_question)
        self.assertEqual(saved_question.id, self.question.id)
        self.assertEqual(saved_question.title, self.question_data["title"])
        self.assertEqual(saved_question.answerRight, self.question_data["answerRight"])
        self.assertEqual(saved_question.options, self.question_data["options"])
        self.assertEqual(saved_question.explanation, self.question_data["explanation"])
        self.assertEqual(saved_question.InQuiz, self.question_data["InQuiz"])

    def test_update_question(self):
        new_question = "What is the capital of Spain?"
        self.question.title = new_question
        self.question.save()

        updated_question = Question.objects.get(id=self.question.id)
        self.assertEqual(updated_question.title,    new_question)
        self.assertEqual(updated_question.answerRight, self.question_data["answerRight"])

    def test_delete_question(self):
        question_id = self.question.id
        self.question.delete()

        with self.assertRaises(Question.DoesNotExist):
            Question.objects.get(id=question_id)

    def test_str(self):
        self.assertEqual(str(self.question), f"{self.question.title} (InQuiz={self.question.InQuiz}, createdAt={self.question.createdAt}, updatedAt={self.question.updatedAt})")

    def test_timestamps(self):
        self.assertIsNotNone(self.question.createdAt)
        self.assertIsNotNone(self.question.updatedAt)
