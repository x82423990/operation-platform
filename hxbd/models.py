from django.db import models


class NodeList(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class NodeInfo(models.Model):
    server_name = models.OneToOneField('NodeList')
    position = models.CharField(max_length=50, help_text="sever所在的位置")
    IP = models.CharField(max_length=100)
    env = models.CharField(max_length=50, help_text="环境")
    job = models.CharField(max_length=50, help_text="所在的工作组")


class MonitorInfo(models.Model):
    server_name = models.ForeignKey(NodeList, on_delete=models.CASCADE)
    load = models.FloatField(max_length=64, help_text="CPU负载")
    count_cpu = models.IntegerField(max_length=8, help_text="CPU 个数")
    total_mem = models.FloatField(max_length=64, help_text="总内存")
    available_mem = models.FloatField(max_length=64, help_text="可用内存")

    def __str__(self):
        return
