import requests
import time
# from datetime import datetime
from django.utils import timezone
from datetime import datetime


class Node:
    def __init__(self):
        # self.args = args
        self.url = "http://192.168.102.60:9090"

    def __retsult(self, data):
        return float(data.get('data').get("result")[-1].get("value")[-1]), float(
            data.get('data').get("result")[-1].get("value")[0])

    def list(self, node=None):
        apiversion = "/api/v1/series"
        if node:
            params = 'instance="%s"' % node
        else:
            params = ""
        args = '?match[]=up{%s}' % params
        url = self.url + apiversion + args
        content = requests.get(url)
        try:
            ret = content.json().get('data')
        except (IndexError, TypeError):
            return None
        return ret

    def cpuinfo(self, instance):
        apiversion_count = "/api/v1/series"
        apiversion_load = "/api/v1/query"
        args = '?match[]=node_cpu_seconds_total{instance="%s"}' % instance
        mem_args = '?query=node_load5{instance="%s"}' % instance
        url = self.url + apiversion_count + args
        mem_url = self.url + apiversion_load + mem_args
        content_cpu = requests.get(url)
        content_load = requests.get(mem_url)
        cpu_count = content_cpu.json().get("data")
        cpu_load = content_load.json()
        cpu = int(len(cpu_count) / 8)
        load, current = self.__retsult(cpu_load)
        return cpu, load, current

    def meminfo(self, instance):
        apiversion = "/api/v1/query"
        args_memtotal = '?query=node_memory_MemTotal_bytes{instance="%s"}' % instance
        urls = self.url + apiversion + args_memtotal
        memTotal = requests.get(urls)
        total_info, _ = self.__retsult(memTotal.json())
        memTotalValue = int(total_info) / 1024 / 1024 / 1024
        # 计算可用
        args_available = '?query=node_memory_MemAvailable_bytes{instance="%s"}' % instance
        mem_available = requests.get(self.url + apiversion + args_available)
        available_info, _ = self.__retsult(mem_available.json())
        mem_available_value = int(available_info) / 1024 / 1024 / 1024
        return memTotalValue, mem_available_value

    def diskinfo(self, instance):
        apiversion = "/api/v1/query?query="
        # 获取磁盘总空间
        total_args = 'node_filesystem_size_bytes{instance="%s", device=~"^/dev/vd[a-z][1-9]$|^/dev/xvd[a-z][1-9]$"}' % instance
        total_info = requests.get(self.url + apiversion + total_args)
        disk_total_value, _ = self.__retsult(total_info.json())
        # 获取可用的磁盘空间
        available_args = 'node_filesystem_avail_bytes{instance="%s", device=~"^/dev/vd[a-z][1-9]$|^/dev/xvd[a-z][1-9]$"}' % instance
        available_info = requests.get(self.url + apiversion + available_args)
        disk_available_value, _ = self.__retsult(available_info.json())
        return disk_total_value, disk_available_value

    # 返回监控数据
    def monitor(self, instance):
        count, load, current = self.cpuinfo(instance)
        total, available = self.meminfo(instance)
        disk_total, available_disk = self.diskinfo(instance)
        monitor = {"count_cpu": count, "load5": load, "total_mem": total, "available_mem": available,
                   "current_time": current, "total_disk": int(disk_total / 1024 / 1024 / 1024),
                   "available_disk": int(available_disk / 1024 / 1024 / 1024)}
        return monitor


if __name__ == '__main__':
    # params = 'node="slave4"'
    # tmp = n.list().get('data')
    #
    # tmp, tmp2, tmp3 = Node().cpuinfo("slave4")
    tmp = Node().list("slave4")
    # for i in tmp:
    #     print(i.get("instance"))
    # tmp, tmp2 = Node().meminfo(instance="slave4")

    # tm4 = Node().monitor("slave4")
    # print(tmp, tmp2, tm4)
    # # ts = 1531721637
    # ts = "2018-07-16 09:48:42.448851"
    # dt = time.strptime(ts, "%Y-%m-%d %H:%M:%S")
    print(tmp)
