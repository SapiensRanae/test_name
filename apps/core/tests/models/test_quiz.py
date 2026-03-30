from django.test import TestCase

from apps.core.models import Creator, Quiz


class QuizModelTest(TestCase):
    def setUp(self):

        self.quiz_data ={
            "title" : "Sample Quiz",
        "description" : "This is a sample quiz for testing.",
        }

        self.creator_data = {"email": "creator@example.com"}

        self.creator = Creator.objects.create(**self.creator_data)
        self.quiz = Quiz.objects.create(**self.quiz_data)

    def test_add_creator(self):
        self.quiz.creator.add(self.creator)
        refreshed_quiz = Quiz.objects.get(id=self.quiz.id)
        self.assertEqual(refreshed_quiz.creator.count(), 1)
        self.assertEqual(refreshed_quiz.creator.first(), self.creator)


    def test_create_quiz(self):
        saved_quiz = Quiz.objects.get(id=self.quiz.id)
        self.assertIsNotNone(saved_quiz)

        self.assertEqual(saved_quiz.title, self.quiz_data["title"])
        self.assertEqual(saved_quiz.description, self.quiz_data["description"])
        self.assertEqual(saved_quiz.maxSeconds, 0)
        self.assertEqual(saved_quiz.maxSecondsPerQuestion, 0)
        self.assertEqual(saved_quiz.creator.count(), 0)
        self.assertIsNotNone(saved_quiz.createdAt)
        self.assertIsNotNone(saved_quiz.updatedAt)



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
