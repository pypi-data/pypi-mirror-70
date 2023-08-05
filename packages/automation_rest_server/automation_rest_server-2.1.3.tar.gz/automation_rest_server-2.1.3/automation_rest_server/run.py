#!/usr/bin/env python
# coding=utf-8
import os
import sys
import re
import argparse
sys.path.append(os.path.join(os.path.dirname(__file__)))
from test_framework.test_pool import TestPool
from test_framework.test_suite import TestSuite
from test_framework.test_case import TestCase
from test_framework.test_environment import Environment
from rest_server.reset_server import *
from rest_server.resource.models.ftp_server import thread_start_ftp_server
from test_framework.database import update_abnormal_end_tests
from test_framework.node_database import update_env_state


def add_sub_argument_group(subparsers, name, handler_function):
    regression_parser = subparsers.add_parser(name, help='%s tests executor'%name)
    regression_required_arguments = regression_parser.add_argument_group('required arguments')
    regression_required_arguments.add_argument('--name', '-n', type=str,
                                               help='test suite ,test case name or operation name',default= "fio", required=False)
    regression_required_arguments.add_argument('--variables', '-v', type=str,  default=None,
                                               help='user variables, format: var1:value1,var2:value3', required=False)
    regression_required_arguments.add_argument('--list', '-l', type=str, default=None,
                                               help='list and filter test case', required=False)
    regression_required_arguments.add_argument('--fw', '-f', type=str, default=None,
                                               help='fw path for upgrade', required=False)
    regression_parser.set_defaults(executor_function=handler_function)


def create_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    add_sub_argument_group(subparsers, 'testsuite', test_suite_handle)
    add_sub_argument_group(subparsers, 'testcase', test_case_handle)
    add_sub_argument_group(subparsers, 'start', start_rest_server)
    return parser


@update_env_state
def get_env_state():
    env = Environment()
    env_information = env.get_environments()
    return env_information


def start_rest_server(args):
    _ = TestPool()
    get_env_state()
    update_abnormal_end_tests()
    thread_start_ftp_server()
    APP.run(host="0.0.0.0")


def test_suite_handle(args):
    test_suite = TestSuite()
    if args.list is not None:
        rets = test_suite.list_and_filter_tests(args.list)
        for item in rets:
            print(item)
    else:
        test_suite.run(args.name)

def test_case_handle(args):
    test_case = TestCase(args.name)
    if args.list is not None:
        rets = test_case.list_and_filter_tests(args.list)
        for item in rets:
            print(item)
    else:
        test_case.run()


def add_globals(args):
    os.environ["root_path"] = os.path.join(os.path.dirname(__file__))
    os.environ["working_path"] = os.getcwd()
    os.environ["PYTHONPATH"] = os.getcwd()
    os.environ['PYTHONUNBUFFERED'] = "TRUE"
    if args.variables is not None:
        str_variable = args.variables
        rets = re.findall("(\w+)\:([^\,]+)", str_variable)
        for item in rets:
            os.environ[str(item[0])] = str(item[1])


def run():
    install_pip_package()
    parser = create_parser()
    args = parser.parse_args()
    try:
        add_globals(args)
        args.executor_function(args)
    except Exception as e:
        print(e)


def get_pip_command():
    if sys.version_info[0] == 2:
        pip_command = "pip"
    else:
        pip_command = "pip3"
    return pip_command


def install_pip_package():
    root_path = os.path.join(os.path.dirname(__file__))
    pip_file = os.path.join(root_path, "pip.txt")
    if os.path.exists(pip_file) is False:
        requirement_file = os.path.join(root_path, "requirements.txt")
        command_str = "{} install -r {}".format(get_pip_command(), requirement_file)
        ret = os.system(command_str)
        if ret != 0:
            print("PIP install failed")
        else:
            fd = open(pip_file, mode="w", encoding="utf-8")
            fd.close()


if __name__ == '__main__':
    run()
