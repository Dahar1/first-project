from django.db import models # type: ignore


# Create your models here.


class Item(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()
    job_title = models.CharField(max_length=50)
    job_experience =  models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

