from django.db import models

# Create your models here.

class MovieData(models.Model):

    title = models.CharField(max_length=200)
    genres = models.CharField(max_length=200)
    index = models.CharField(max_length=200, primary_key=True)

    class Meta:
        db_table = 'movie_data'
        managed = False

