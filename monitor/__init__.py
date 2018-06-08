from aliyunsdkcore import client
from aliyunsdkcms.request.v20180308 import QueryMetricListRequest
import time

clt = client.AcsClient(
    "LTAIM5QslSSa2nqv",
    "rHBjTNtOVqkxVEIOg8JzPrLi6rShBo",
    "cn-shenzhen"
)
request = QueryMetricListRequest.QueryMetricListRequest()
request.set_accept_format('json')
request.set_Project('acs_ecs_dashboard')
request.set_Metric('CPUUtilization')
start_time = "2018-05-25 10:00:00"
timestamp_start = int(time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S"))) * 1000
request.set_StartTime(timestamp_start)
request.set_Dimensions("{'instanceId':'i-94g5hc378'}")
request.set_Period('60')
result = clt.do_action_with_exception(request)
print(result)
