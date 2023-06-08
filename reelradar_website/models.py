from django.db import models


class MovieData(models.Model):

    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    index = models.CharField(max_length=200, primary_key=True)

    class Meta:
        db_table='movie_data'


