import json
import os

import thriftpy
from thriftpy.rpc import make_client


def make_service(host, port, timeout=10000):
    RESOURCE_OF_THRIFT, _ = os.path.split(os.path.abspath(__file__))
    thrift_path = RESOURCE_OF_THRIFT + "/client.thrift"
    profiling_client = thriftpy.load(thrift_path, module_name="p_thrift")

    global client
    client = make_client(profiling_client.ProfilingService, host, port, timeout=timeout)


def build_query(merchant_id, business_case_id, s_filter):
    if client:
        return client.build_query(merchant_id, business_case_id, s_filter)
    raise ModuleNotFoundError("No client here. Please run make_service first")


def add_user(merchant_id, source, data, business_case_id=None):
    if client:
        data_json_str = ''
        if data:
            data_json_str = json.dumps(data)
        return client.add_user(merchant_id, source, data_json_str, business_case_id)
    raise ModuleNotFoundError("No client here. Please run make_service first")


def add_user_b2b(merchant_id, source, data, business_case_id=None):
    if client:
        data_json_str = ''
        if data:
            data_json_str = json.dumps(data)
        return client.add_user_b2b(merchant_id, source, data_json_str, business_case_id)
    raise ModuleNotFoundError("No client here. Please run make_service first")


def change_state_user(merchant_id, profile_id, state):
    if client:
        return client.change_state_user(merchant_id, profile_id, state)
    raise ModuleNotFoundError("No client here. Please run make_service first")


def add_update_merge_profile(merchant_id, source, data, business_case_id):
    if client:
        return client.add_update_merge_profile(merchant_id, source, data, business_case_id)
    raise ModuleNotFoundError("No client here. Please run make_service first")


def test():
    if client:
        return client.test()
    raise ModuleNotFoundError("No client here. Please run make_service first")
