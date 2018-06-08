import requests


class Monitor:
    def __init__(self, url):
        self.url = url

    def node_count(self):
        api = self.url + "/api/v1/query?query=up"
        ret = requests.get(api)
        data = ret.json().get("data").get("result")
        return len(data)

    def up_node_count(self):
        api = self.url + "/api/v1/query?query=up"
        ret = requests.get(api)
        data = ret.json().get("data").get("result")
        count = 0
        for i in data:
            j = i.get('value')
            if j[-1] == "1":
                count += 1
        return count

    def instance(self):
        api = self.url + "/api/v1/query?query=up"
        ret = requests.get(api)
        data = ret.json().get("data").get("result")
        instan_list = []
        for i in data:
            j = i.get('value')
            if j[-1] == "1":
                instan_list.append(i.get('metric').get('instance'))
        return instan_list

    def pre_cpu(self):
        res = []
        amoust = 0
        for i in self.instance():
            api = "/api/v1/series?match[]=node_cpu_seconds_total{instance= \"%s\"}" % i
            ret = requests.get(self.url + api)
            count = ret.json().get("data")
            tmp = []
            for j in count:
                if j.get("cpu") not in tmp:
                    tmp.append(j.get("cpu"))
            res.append({i: len(tmp)})
            amoust += len(tmp)
        return {"total": amoust, "data": res}

    def load5(self):
        api = self.url + "/api/v1/query?query=node_load5"
        ret = requests.get(api)
        data = ret.json().get("data").get("result")
        res = []
        total = 0
        for i in data:
            instance = i.get("metric").get("instance")
            val = i.get("value")[-1]
            res.append({instance: val})
            total += float(val)
        return {"total": total, "data": res}

    def mem_total(self):
        api = self.url + "/api/v1/query?query=node_memory_MemTotal_bytes"
        ret = requests.get(api)
        data = ret.json().get("data").get("result")
        res = []
        total = 0
        for i in data:
            instance = i.get("metric").get("instance")
            val = float(i.get("value")[-1]) / 1000 / 1024
            res.append({instance: val})
            total += float(val)
        return {"total": total, "data": res}

    def mem_available(self):
        api = self.url + "/api/v1/query?query=node_memory_MemAvailable_bytes"
        ret = requests.get(api)
        data = ret.json().get("data").get("result")
        res = []
        total = 0
        for i in data:
            instance = i.get("metric").get("instance")
            val = float(i.get("value")[-1]) / 1000 / 1024
            res.append({instance: val})
            total += float(val)
        return {"total": total, "data": res}


a = Monitor("http://192.168.102.60:9090")
# print(a.pre_cpu())
print(a.mem_available())
