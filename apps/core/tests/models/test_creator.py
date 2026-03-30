from django.test import TestCase

from apps.core.models import Creator

class CreatorTest(TestCase):
    def setUp(self):
        self.creator_data ={
            "email": "example@email.com"
        }
        self.creator = Creator.objects.create(**self.creator_data)

    def test_create_creator(self):
        saved_creator = Creator.objects.get(id=self.creator.id)
        self.assertIsNotNone(saved_creator)
        self.assertEqual(saved_creator.id, self.creator.id)
        self.assertEqual(saved_creator.email, self.creator.email)

    def test_update_creator(self):
        new_email = "example2@email.com"
        self.creator.email = new_email
        self.creator.save()

        updated_creator = Creator.objects.get(id=self.creator.id)
        self.assertEqual(updated_creator.email, new_email)

    def test_delete_creator(self):
        creator_id = self.creator.id
        self.creator.delete()

        with self.assertRaises(Creator.DoesNotExist):
            Creator.objects.get(id=creator_id)

    def test_str(self):
        self.assertEqual(str(self.creator), f"{self.creator.email} (createdAt={self.creator.createdAt}, updatedAt={self.creator.updatedAt})")

    def test_timestamps(self):
        self.assertIsNotNone(self.creator.createdAt)
        self.assertIsNotNone(self.creator.updatedAt)