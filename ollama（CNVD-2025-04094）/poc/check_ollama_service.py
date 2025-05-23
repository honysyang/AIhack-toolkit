# 定义 banner
BANNER = r"""
██████╗ ██╗   ██╗███████╗███████╗██████╗ 
██╔══██╗██║   ██║██╔════╝██╔════╝██╔══██╗
██████╔╝██║   ██║███████╗█████╗  ██████╔╝
██╔══██╗██║   ██║╚════██║██╔══╝  ██╔══██╗
██████╔╝╚██████╔╝███████║███████╗██║  ██║
╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝
Ollama 服务检测脚本
"""

import requests
from typing import Union
import argparse
import ipaddress
import concurrent.futures
from tqdm import tqdm
from threading import Lock

print_log = True
message = ""
lock = Lock()

# 修改 main 函数
def main() -> None:
    global message
    print(BANNER)
    parser = argparse.ArgumentParser(description='检测指定 IP 或网段的 Ollama 服务')
    parser.add_argument('--ip', type=str, required=True, help='要检测的 Ollama 服务的 IP 地址或网段，例如：192.168.1.1 或 192.168.1.0/24')
    parser.add_argument('-v', action='store_true', help='打印扫描日志')
    args = parser.parse_args()
    global print_log
    print_log = args.v
    process_target(args.ip)
    if message.strip():
        print(message)
    else:
        print(f" \n未发现任何 Ollama 服务")

def check_ollama_service(ip: str) -> None:
    global message
    try:
        response = requests.get(f'http://{ip}:11434/api/tags', timeout=5)
        response.raise_for_status()
        if print_log:
            print(f"IP {ip} 的 Ollama 服务正在运行")
        with lock:
            message += f"IP {ip} 的 Ollama 服务正在运行 \n"
        check_delete_api(ip)
    except requests.ConnectionError:
        if print_log:
            print(f"无法连接到 IP {ip} 的 Ollama 服务")
    except requests.Timeout:
        if print_log:
            print(f"连接 IP {ip} 的 Ollama 服务超时")
    except requests.RequestException as e:
        if print_log:
            print(f"访问 IP {ip} 的 Ollama 服务时发生错误: {e}")

def check_delete_api(ip: str) -> None:
    global message
    try:
        delete_response = requests.delete(f'http://{ip}:11434/api/delete?model=example_model', timeout=5)
        try:
            response_json = delete_response.json()
            if 'error' in response_json:
                if print_log:
                    print(f"警告：IP {ip} 的 Ollama 服务存在未授权漏洞")
                    print("具体特征为：攻击者可未授权访问 Ollama 服务的 API，实现删除模型等操作")
                with lock:
                    message += f"警告：IP {ip} 的 Ollama 服务存在未授权漏洞CNVD-2025-04094 \n"
                    message += "具体特征为：攻击者可未授权访问 Ollama 服务的 API，实现删除模型等操作 \n"
            else:
                if print_log:
                    print(f"IP {ip} 的 Ollama 服务存在API可连接，可能存在未授权访问的安全风险")
                with lock:
                    message += f"IP {ip} 的 Ollama 服务存在API可连接，可能存在未授权访问CNVD-2025-04094的安全风险 \n"
        except ValueError:
            if print_log:
                print(f"IP {ip} 的 Ollama 删除模型 API 返回内容不是有效的 JSON 格式")
    except requests.RequestException:
        if print_log:
            print(f"IP {ip} 的 Ollama 删除模型 API 可能不存在。")

def process_target(target: str) -> None:
    """
    处理用户输入的目标（单个 IP 或网段）并进行检测。
    :param target: 要检测的 IP 地址或网段
    """
    try:
        network = ipaddress.ip_network(target, strict=False)
        ip_list = [str(ip) for ip in network.hosts()]
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # 使用 tqdm 创建进度条
            list(tqdm(executor.map(check_ollama_service, ip_list), total=len(ip_list), desc="扫描进度"))
    except ValueError:
        try:
            ip = ipaddress.ip_address(target)
            check_ollama_service(str(ip))
        except ValueError:
            print("输入的目标既不是有效的 IP 地址也不是有效的网段")

if __name__ == "__main__":
    main()