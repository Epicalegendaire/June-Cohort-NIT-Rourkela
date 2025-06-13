from django.db import models

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    diagnosis = models.CharField(max_length=200)
    history = models.TextField()

    def __str__(self):
        return self.name