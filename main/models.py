from django.db import models

class Poll(models.Model):
    question = models.CharField(max_length=200)

class AuthToken(models.Model):
    code = models.TextField()

class Person(models.Model):
    fid = models.IntegerField(primary_key=True)
    name = models.TextField()

class Compatibility(models.Model):
    f1_id = models.IntegerField()
    f1_name = models.TextField()
    f2_id = models.IntegerField()
    f2_name = models.TextField()
    rater = models.IntegerField()
    rater_name = models.TextField()
    rating = models.IntegerField()


