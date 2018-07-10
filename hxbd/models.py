from django.db import models


class NodeList(models.Model):
    server_name = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    IP = models.CharField(max_length=100)
    env = models.CharField(max_length=50)
    job = models.CharField(max_length=50)


class NodeInfo(models.Model):
    artist = models.ForeignKey(NodeList, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    num_stars = models.IntegerField()
