from django.db import models

class clients(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    client = models.CharField(max_length=200)
    priority = models.IntegerField()
    date = models.DateField()
    area = models.CharField(max_length=200)

    def __str__(self):
        return self.title




