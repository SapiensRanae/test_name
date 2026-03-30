from django.test import TestCase

from apps.core.models import CQuiz, Creator, Quiz

class CQuizTest(TestCase):
    def setUp(self):
        self.creator_data ={
            "email": "creator@email.com",
        }
        self.quiz_data ={
            "title": "quiz name",
            "description": "description"
        }
        self.cquiz_data ={
            "trueAnswersP": 0,
            "triedTimes": 0,
        }

        self.creator = Creator.objects.create(**self.creator_data)
        
        # Create CQuiz directly. It will create the underlying Quiz as well.
        # We merge quiz_data and cquiz_data.
        self.cquiz = CQuiz.objects.create(**self.quiz_data, **self.cquiz_data)
        self.cquiz.creator.add(self.creator)

    def test_create_cquiz(self):
        saved_cquiz = CQuiz.objects.get(id=self.cquiz.id)
        self.assertIsNotNone(saved_cquiz)
        self.assertEqual(saved_cquiz.id, self.cquiz.id)
        self.assertEqual(saved_cquiz.trueAnswersP, self.cquiz_data["trueAnswersP"])
        self.assertEqual(saved_cquiz.triedTimes, self.cquiz_data["triedTimes"])
        self.assertEqual(saved_cquiz.title, self.quiz_data["title"])

    def test_update_cquiz(self):
        new_trueAnswersP = 50
        self.cquiz.trueAnswersP = new_trueAnswersP
        self.cquiz.save()

        updated_cquiz = CQuiz.objects.get(id=self.cquiz.id)
        self.assertEqual(updated_cquiz.trueAnswersP, new_trueAnswersP)
        self.assertEqual(updated_cquiz.triedTimes, self.cquiz_data["triedTimes"])

    def test_delete_cquiz(self):
        cquiz_id = self.cquiz.id
        self.cquiz.delete()

        with self.assertRaises(CQuiz.DoesNotExist):
            CQuiz.objects.get(id=cquiz_id)

    def test_str(self):
        self.assertEqual(str(self.cquiz), f"cquiz(id={self.cquiz.id}, title={self.cquiz.title}, trueAnswersP={self.cquiz.trueAnswersP}, startedAt={self.cquiz.startedAt}, finishedAt={self.cquiz.finishedAt})")

    def test_timestamps(self):
        self.assertIsNotNone(self.cquiz.createdAt)
        self.assertIsNotNone(self.cquiz.updatedAt)


