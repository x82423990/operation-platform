from django.db import models


# import django.utils.timezone as timezone


class Node(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class NodeInfo(models.Model):
    server_name = models.OneToOneField('Node', on_delete=models.CASCADE)
    position = models.CharField(max_length=50, help_text="sever所在的位置")
    IP = models.CharField(max_length=100)
    env = models.CharField(max_length=50, help_text="环境")
    job = models.CharField(max_length=50, help_text="所在的工作组")

    class Meta:
        db_table = "nodeinfo"


class MonitorInfo(models.Model):
    server_name = models.ForeignKey("Node", on_delete=models.CASCADE)
    load = models.FloatField(max_length=64, help_text="CPU负载")
    count_cpu = models.IntegerField(help_text="CPU 个数")
    total_mem = models.FloatField(max_length=64, help_text="总内存")
    total_disk = models.FloatField(max_length=64, help_text="总磁盘")
    available_disk = models.FloatField(max_length=64, help_text="可用磁盘")
    available_mem = models.FloatField(max_length=64, help_text="可用内存")
    get_time = models.DateTimeField(auto_now_add=True, help_text="时间")

    def __str__(self):
        return self.load

    class Meta:
        db_table = "monitorinfo"
