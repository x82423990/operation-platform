import requests


class Node:
    def __init__(self):
        # self.args = args
        self.url = "http://192.168.102.60:9090"

    def __retsult(self, data):
        return float(data.get('data').get("result")[-1].get("value")[-1])

    def list(self, node=None):
        apiversion = "/api/v1/series"
        if node:
            params = 'instance="%s"' % node
        else:
            params = ""
        args = '?match[]=up{%s}' % params
        print(args)
        url = self.url + apiversion + args
        print(url)
        content = requests.get(url)
        # print(content.json())
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
        # print(cpu)
        # print(self.__retsult(cpu_load))
        return cpu, self.__retsult(cpu_load)

    def meminfo(self, instance):
        apiversion = "/api/v1/query"
        args_memtotal = '?query=node_memory_MemTotal_bytes{instance="%s"}' % instance
        memTotal = requests.get(self.url + apiversion + args_memtotal)
        memTotalValue = int(self.__retsult(memTotal.json())) / 1024 / 1024 / 1024

        # 计算可用
        args_available = '?query=node_memory_MemAvailable_bytes{instance="%s"}' % instance
        mem_available = requests.get(self.url + apiversion + args_available)
        mem_available_value = int(self.__retsult(mem_available.json())) / 1024 / 1024 / 1024

        return memTotalValue, mem_available_value


if __name__ == '__main__':

    params = 'node="slave4"'
    # tmp = n.list().get('data')
    #
    # tmp, tmp2 = n.cpuinfo(instance="slave4")
    tmp = Node().list()
    for i in tmp:
        print(i.get("instance"))
    # tmp, tmp2 = n.meminfo(instance="slave4")
    # print(tmp)
