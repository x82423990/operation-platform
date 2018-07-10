import requests


class Node:
    def __init__(self):
        # self.args = args
        self.url = "http://192.168.102.60:9090"

    def __retsult(self, data):
        return data.get('data').get("result")[-1].get("value")[-1]

    def list(self, condition=""):
        apiversion = "/api/v1/series"
        args = '?match[]=up{%s}' % condition
        url = self.url + apiversion + args
        content = requests.get(url)
        print(content.json())

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
        print(cpu)
        print(self.__retsult(cpu_load))

    def meminfo(self, instance):
        apiversion = "/api/v1/query"
        args_memtotal = '?query=node_memory_MemTotal_bytes{instance="%s"}' % instance
        # args_memavb =
        memTotal = requests.get(self.url + apiversion + args_memtotal)
        memTotalValue = int(self.__retsult(memTotal.json()))/1024/1024/1024

        # 计算可用
        args_available = '?query=node_memory_MemAvailable_bytes{instance="%s"}' % instance
        mem_available = requests.get(self.url + apiversion + args_available)
        mem_available_value = int(self.__retsult(mem_available.json()))/1024/1024/1024

        print(memTotalValue, mem_available_value)


if __name__ == '__main__':

    n = Node()
    params = 'instance="slave4"'
    # n.list(condition=params)
    n.cpuinfo(instance="slave4")
    n.list(condition=params)
    n.meminfo(instance="slave4")
