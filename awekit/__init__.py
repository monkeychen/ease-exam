import os
import sys
from typing import List
import platform
import subprocess
import time
import argparse
from datetime import datetime
from dateutil import relativedelta

UTF_8 = "UTF-8"
UTF8 = "UTF8"
GBK = "GBK"
DEF_DATE_FMT = "%Y-%m-%d %H:%M:%S"


def add_cwd_to_syspath(print_path=False):
    cwd_path = os.getcwd()
    if cwd_path not in sys.path:
        sys.path.insert(1, os.getcwd())
    if print_path:
        print(f"{'~~~' * 25} Python Search Path {'~~~' * 25}")
        print(f"The sys.path = {sys.path}")
        print("~~~" * 60)


def add_dir_to_syspath(base_dir_path=os.getcwd()):
    if base_dir_path is None:
        base_dir_path = "/wg_cmcc/apps/fmcc-awesome-kit"
    if base_dir_path not in sys.path:
        sys.path.append(base_dir_path)
    print(f"sys.path={sys.path}")


def is_windows():
    return platform.system() not in ("Linux", "Darwin")


def is_linux():
    return platform.system() == "Linux"


def is_macos():
    return platform.system() == "Darwin"


def get_timestamp(fmt="%Y%m%d%H%M%S"):
    return datetime.now().strftime(fmt)


def method_time_elapsed(method):
    def wrapper(self, *args, **kwargs):
        b_t = time.time()
        res = method(self, *args, **kwargs)
        e_t = time.time()
        print(f"It has took {round(e_t - b_t, 3)}s to invoke this [{method.__name__}] method!")
        return res
    return wrapper


def func_time_elapsed(func):
    def wrapper(*args, **kwargs):
        b_t = time.time()
        res = func(*args, **kwargs)
        e_t = time.time()
        print(f"It has took {round(e_t - b_t, 3)}s to invoke this [{func.__name__}] method!")
        return res
    return wrapper


def exec_shell_cmd(cmd, dt_flag=None, encoding=UTF_8):
    b_t = time.time()
    cmd_id = dt_flag
    if cmd_id is None:
        cmd_id = get_timestamp()
    print(f"cmd[id = {cmd_id}] => {cmd}")
    exec_result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result_str = str(exec_result.stdout, encoding=encoding).strip()
    e_t = time.time()
    print(f"Shell script[cmd_id = {cmd_id}, cost_time = {round(e_t - b_t, 2)}s]'s execution result is: \n{result_str}")
    return result_str, result_str.lower().find("error") == -1


def readline(file_path, encoding=UTF_8, limit=-1):
    with open(file_path, mode='r', encoding=encoding) as fr:
        if limit <= 0:
            return fr.readlines()
        else:
            lines = []
            while len(lines) < limit:
                lines.append(fr.readline())
            return lines


def read_from_file(file_path, params: dict = None, encoding=UTF_8):
    content = ""
    try:
        with open(file_path, mode='r', encoding=encoding) as fr:
            original_content = fr.read()
        content = original_content
        if params is not None:
            content = original_content.format(**params)
    except Exception:
        print(f"Fail to read from file:{file_path}")
    return content


def write_to_file(file_path, content: str, encoding=UTF_8):
    try:
        with open(file_path, mode='w', encoding=encoding) as fw:
            fw.write(content)
    except Exception:
        print(f"Fail to write to file:{file_path}")
        return False
    return True


class ArgConf(object):
    def __init__(self, flag, name, action=None, nargs=None, arg_type=None, choices=None, default=None, tip=None):
        self.flag = flag
        self.name = name
        self.action = action
        self.nargs = nargs
        self.arg_type = arg_type
        self.choices = choices
        self.default = default
        self.tip = tip


def parse_cli_args(show_args=True, extra_args: List[ArgConf] = None):
    scheduled_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    def_date_id = (datetime.today() - relativedelta.relativedelta(days=1)).strftime("%Y%m%d")

    cli_parser = argparse.ArgumentParser(description="这是一个有用的小工具。", add_help=False)
    cli_parser.add_argument('-b', '--base_dir_path', nargs='?', default="/wg_cmcc/apps/fmcc-awesome-kit", help='工作空间所在目录路径。')
    cli_parser.add_argument('-d', '--date_id', nargs='?', type=int, default=def_date_id, help='上报日期（天），格式为yyyyMMdd，默认为昨天。')
    cli_parser.add_argument('-e', '--env_mode', nargs='?', choices=['dev', 'prod'], default='prod',
                            help='设置运行环境（dev：开发环境，prod：生产环境），默认为生产环境')
    cli_parser.add_argument('-h', '--help', action='help', help='显示本帮助信息并退出')
    cli_parser.add_argument('-v', '--version', action='version', version='%(prog)s V0.0.1', help='显示当前版本信息并退出')
    if extra_args is not None and len(extra_args) > 0:
        for extra_arg in extra_args:
            parse_extra_arg(parser=cli_parser, arg_conf=extra_arg)

    args = cli_parser.parse_args()
    if show_args:
        print(f"The programme[{cli_parser.prog}] was scheduled at {scheduled_time}, cwd = {os.getcwd()}, env_mode = {args.env_mode}, "
              f"base_dir_path = {args.base_dir_path}, date_id = {args.date_id}")
    return args


def parse_extra_arg(parser: argparse.ArgumentParser, arg_conf: ArgConf):
    kwargs = {}
    if arg_conf.action is not None:
        kwargs["action"] = arg_conf.action
    if arg_conf.nargs is not None:
        kwargs["nargs"] = arg_conf.nargs
    if arg_conf.arg_type is not None:
        kwargs["type"] = arg_conf.arg_type
    if arg_conf.choices is not None:
        kwargs["choices"] = arg_conf.choices
    if arg_conf.default is not None:
        kwargs["default"] = arg_conf.default
    if arg_conf.tip is not None:
        kwargs["help"] = arg_conf.tip
    parser.add_argument(arg_conf.flag, arg_conf.name, **kwargs)


def make_parent_dirs(file_path: str):
    dir_path = os.path.dirname(file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def pid_of(process_name: str, excludes: list = None) -> int:
    if is_windows():
        print("Not support Windows-OS!")
        return -2
    cmd = f"ps -ef | grep '{process_name}' | grep -v grep"
    if excludes is not None and len(excludes) > 0:
        for word in excludes:
            cmd = cmd + f" | grep -v '{word}' "
    out, _ = exec_shell_cmd(cmd)
    pids = [line.split()[1] for line in out.splitlines()]
    return int(pids[0]) if len(pids) == 1 else -1


