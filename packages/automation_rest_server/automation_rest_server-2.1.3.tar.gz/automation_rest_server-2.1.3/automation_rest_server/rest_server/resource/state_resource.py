# coding=utf-8
import sys
import os
from flask_restful import Resource
from flask_restful import marshal_with
from rest_server.resource.models.helper import resource_fields
from test_framework.test_pool import TestPool
from utils.system import get_ip_address, get_linux_nvme_devs
from test_framework.state import State
from tool.device import NVME


class StateResource(Resource):

    def __init__(self):
        self.test_pool = TestPool()

    @staticmethod
    def get_automation_platform():
        work_path = os.environ["working_path"]
        if "test-platform" in work_path.lower():
            platform = "oakgate"
        elif "production" in work_path.lower() or "perses" in work_path.lower():
            platform = "perses"
        elif "venus" in work_path.lower():
            platform = "venus"
        else:
            platform = "none"
        return platform

    @marshal_with(resource_fields, envelope='resource')
    def get(self):
        data = []
        state = self.test_pool.get_env_state()
        ip_ = get_ip_address()
        if "win" in sys.platform:
            system_name = "windows"
            device = NVME()
            dev_list = device.list_dev()
        else:
            system_name = "linux"
            dev_list = get_linux_nvme_devs()
        data.append(state)
        data.append(ip_)
        data.append(system_name)
        if not dev_list:
            dev_list = list()
            dev = {"index": -1, "name": "not find device"}
            dev_list.append(dev)
        data.append(dev_list)
        data.append(self.get_automation_platform())
        result = {
            "data": data,
            "state": State.PASS
        }
        return result
