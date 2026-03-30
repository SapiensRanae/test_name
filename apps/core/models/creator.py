from django.db import models




class Creator(models.Model):
    # main fields

    email = models.EmailField(unique=True, null=False, blank=False)


    #metadata fields
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    # connections
    #in quiz model
    #ownedQuizzes = models.ManyToManyField(Quiz, blank=True)

    # getters, setters and overwrites

    def __str__(self)-> str:
        return (
            f"{self.email}"
            f" (createdAt={self.createdAt}, updatedAt={self.updatedAt})")
