from django.db import models

class Question(models.Model):
    # main fields

    # can be added automatically by django, but it's gonna be BigAutoField (long), and we want AutoField (int) for optimization purposes
    # can be changed in config
    id = models.AutoField(primary_key=True)

    title = models.CharField(max_length=255)

    #index of answer options
    answerRight = models.IntegerField()
    answerOptions = models.TextField()  # JSON string of answer options

    maxSecondsPerQuestion = models.IntegerField(default=0)

    explanation = models.TextField()  # optional field for additional information

    #connections
    InQuiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name='questions')

    #metadata fields
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    # getters, setters and overwrites


    def __str__(self)-> str:
        return {
            f"{self.title}"
            f" (InQuiz={self.InQuiz}, createdAt={self.createdAt}, updatedAt={self.updatedAt})"
        }
