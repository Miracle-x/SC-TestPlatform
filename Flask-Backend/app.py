import shutil
import threading

import yaml
from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os
import logging
from urllib.parse import urlparse
import time
from datetime import datetime
import uuid
from threading import Thread
from collections import defaultdict
from flask_cors import CORS

# 配置简单的日志格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

######################################################################################################################
# k8s场景管理
######################################################################################################################
from kubernetes import client, config

config.load_kube_config()


@app.route('/namespace/<string:namespace>', methods=['GET'])
def check_namespace(namespace):
    v1 = client.CoreV1Api()
    namespaces = v1.list_namespace()

    for ns in namespaces.items:
        if ns.metadata.name == namespace:
            return jsonify({"exists": True}), 200

    return jsonify({"exists": False}), 200


@app.route('/deploy', methods=['POST'])
def deploy_namespace():
    data = request.json
    namespace = data.get('namespace')

    if not namespace:
        return jsonify({"error": "Namespace is required."}), 400

    # 创建 namespace
    v1 = client.CoreV1Api()
    ns_body = client.V1Namespace(metadata=client.V1ObjectMeta(name=namespace))

    try:
        v1.create_namespace(ns_body)
    except client.exceptions.ApiException as e:
        if e.status == 409:
            logger.info({"message": f"Namespace '{namespace}' already exists."}), 200
        else:
            logger.info({"error": f"Failed to create namespace '{namespace}': {e.reason}"}), 500

    # 读取 YAML 文件
    yaml_file_path = f"yaml/{namespace}.yaml"

    if not os.path.exists(yaml_file_path):
        return jsonify({"error": f"YAML file for namespace '{namespace}' does not exist."}), 404

    with open(yaml_file_path, 'r') as f:
        yaml_documents = list(yaml.safe_load_all(f))  # 使用 safe_load_all 加载所有文档

    # 部署 Kubernetes 资源
    k8s_client = client.ApiClient()
    for resource in yaml_documents:
        # 确保资源不为空，且具有 'kind' 和 'apiVersion'
        if resource and 'kind' in resource and 'apiVersion' in resource:
            api_version = resource['apiVersion']
            kind = resource['kind'].lower()

            if kind == 'subnet':
                # 处理 Subnet 自定义资源
                api_path = f'/apis/kubeovn.io/v1/subnets'
                response_type = 'V1Subnet'
            else:
                # 处理其他 Kubernetes 资源
                api_path = f'/apis/{api_version}/namespaces/{namespace}/{kind}s'
                response_type = f'V1{kind.capitalize()}'

            try:
                k8s_client.call_api(
                    api_path,
                    'POST',
                    body=resource,
                    response_type=response_type,
                    _preload_content=False
                )
            except client.exceptions.ApiException as e:
                logger.info(
                    {"error": f"Failed to deploy {kind.capitalize()} in namespace '{namespace}': {e.reason}"}), 500
        else:
            return jsonify({"error": "Invalid resource in YAML."}), 400

    return jsonify({"message": f"Deployment for namespace '{namespace}' initiated.", "status": True}), 201


######################################################################################################################
# Nuclei
######################################################################################################################


# 存储扫描状态的字典
scan_status = {}
# 存储扫描结果的字典
scan_results = defaultdict(list)
# 存储扫描详细信息的字典
scan_details = {}


def validate_url(url):
    """验证并格式化URL"""
    if not url.startswith(('http://', 'https://')):
        url = f'http://{url}'
    try:
        result = urlparse(url)
        return bool(result.netloc), url
    except Exception:
        return False, url


def process_nuclei_output(line):
    """处理nuclei输出行"""
    if not line:
        return None

    line = line.strip()
    if not line:
        return None

    if line.startswith("ERROR: "):
        line = line[7:]
    return line


# 创建一个全局锁
lock = threading.Lock()


def run_scan(scan_id, type, target_url, severity, template_path):
    """在后台运行扫描"""
    try:
        scan_status[scan_id]['status'] = 'running'
        scan_start_time = time.time()
        scan_details[scan_id]['start_time'] = datetime.now().isoformat()  # 确保记录开始时间

        now = datetime.now()
        current_time_str = now.strftime("%Y-%m-%d_%H:%M:%S")
        result_name = 'output_reports/' + target_url.replace('://', '') + '_' + current_time_str

        os.makedirs(result_name, exist_ok=True)

        # 复制文件
        shutil.copy('result_report.pdf', result_name)

        # 构建nuclei命令
        if type != 'agent':
            cmd = [
                'nuclei',
                '-u', target_url,
                '-severity', severity,
                '-t', template_path,
                '-debug'
            ]
        else:
            cmd = ['python', '../AutoGen-CTF/tests/agent_test/test_code_exec_agent/test_code_exec_agent.py', '-msg',
                   f'验证{target_url}的漏洞是否存在，你可以在知识库中找到相关信息']

        logger.info(f"执行命令: {' '.join(cmd)}")

        # 执行命令
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            bufsize=1,
            encoding='utf-8',  # 设置编码
            errors='replace'  # 处理解码错误
        )

        template_results = []
        vulnerability_results = []

        while True:
            logger.info(scan_details[scan_id])
            output = process.stderr.readline()
            if output:
                line = process_nuclei_output(output)
                if line:
                    logger.info(f"输出: {line}")

                    with lock:
                        scan_results[scan_id].append(line)
                        scan_results[scan_id] = scan_results[scan_id][-100:]
                        # 更新scan_details
                        # scan_details[scan_id]['current_output'] = scan_results[scan_id]  # 更新当前输出
                        scan_details[scan_id]['status'] = 'running'  # 确保状态是运行中
                    if '[INF]' in line:
                        template_results.append(line)
                    elif '[VLN]' in line:
                        vulnerability_results.append(line)
                        logger.critical(f"发现漏洞: {line}")

            error = process.stderr.readline()
            if error:
                line = process_nuclei_output(error)
                if line:
                    logger.info(f"输出: {line}")

                    with lock:
                        scan_results[scan_id].append(line)
                        # 更新scan_details
                        # scan_details[scan_id]['current_output'] = scan_results[scan_id]  # 更新当前输出
                        scan_details[scan_id]['status'] = 'running'  # 确保状态是运行中

            if output == '' and error == '' and process.poll() is not None:
                break

        return_code = process.poll()
        scan_end_time = time.time()
        scan_duration = round(scan_end_time - scan_start_time, 2)

        # 更新扫描状态和结果
        with lock:
            scan_details[scan_id].update({
                'status': 'completed',
                'scan_duration': scan_duration,
                'findings': scan_results[scan_id],
                'template_executions': template_results,
                'vulnerabilities': vulnerability_results,
                'total_findings': len(scan_results[scan_id]),
                'exit_code': return_code
            })
            scan_status[scan_id]['status'] = 'completed'

        logger.info(f"扫描完成！用时: {scan_duration} 秒")

    except Exception as e:
        logger.exception("扫描过程中发生错误")
        with lock:
            scan_status[scan_id]['status'] = 'error'
            scan_details[scan_id].update({
                'status': 'error',
                'error': str(e)
            })


@app.route('/scan', methods=['GET', 'POST'])
def scan():
    """启动新的扫描任务"""
    try:
        # 获取参数
        if request.method == 'GET':
            target_url = request.args.get('url')
            type = request.args.get('type', 'nuclei')
            severity = request.args.get('severity', 'critical,high')
            template_path = request.args.get('template', '/root/nuclei-templates/http/cves/2024')
        else:  # POST
            data = request.get_json() or {}
            target_url = data.get('url')
            type = request.args.get('type', 'nuclei')
            severity = data.get('severity', 'critical,high')
            template_path = data.get('template', '/root/nuclei-templates/http/cves/2024')

        # 验证必需参数
        if not target_url:
            return jsonify({
                'status': 'error',
                'message': 'Target URL is required'
            }), 400

        # 验证并格式化URL
        is_valid, formatted_url = validate_url(target_url)
        if not is_valid:
            return jsonify({
                'status': 'error',
                'message': f'Invalid URL: {target_url}'
            }), 400

        # 检查模板目录是否存在
        print(template_path)
        if not os.path.exists(template_path):
            return jsonify({
                'status': 'error',
                'message': f'Template directory not found: {template_path}'
            }), 400

        # 生成唯一的扫描ID
        scan_id = str(uuid.uuid4())

        # 初始化扫描状态
        scan_status[scan_id] = {
            'status': 'initializing',
            'start_time': datetime.now().isoformat()
        }

        # 初始化扫描详情
        scan_details[scan_id] = {
            'status': 'initializing',
            'target_url': formatted_url,
            'severity': severity,
            'template': template_path,
            'start_time': datetime.now().isoformat(),
            'start_time_time': time.time(),
            'scan_duration': 0,
        }

        # 在新线程中启动扫描
        Thread(target=run_scan, args=(scan_id, type, formatted_url, severity, template_path)).start()

        # 返回扫描ID
        return jsonify({
            'status': 'accepted',
            'message': 'Scan started',
            'scan_id': scan_id
        })

    except Exception as e:
        logger.exception("启动扫描任务时发生错误")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/scan/status/<scan_id>', methods=['GET'])
def get_scan_status(scan_id):
    """获取扫描状态"""
    try:
        if scan_id not in scan_status:
            return jsonify({
                'status': 'error',
                'message': 'Scan ID not found'
            }), 404

        # 获取基本状态信息
        status = scan_status[scan_id]['status']

        scan_details[scan_id].update({
            'scan_duration': round(time.time() - scan_details[scan_id]['start_time_time'], 2)
        })
        # 获取详细信息
        details = scan_details.get(scan_id, {})

        # 获取当前结果
        current_results = scan_results.get(scan_id, [])

        response = {
            'scan_id': scan_id,
            'status': status,
            'details': details,
            'current_results': current_results,
            'total_results_count': len(current_results)
        }

        # 如果扫描已完成，清理不再需要的数据
        if status == 'completed':
            scan_results.pop(scan_id, None)

        return jsonify(response)

    except Exception as e:
        logger.exception("获取扫描状态时发生错误")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/scan/list', methods=['GET'])
def list_scans():
    """列出所有扫描任务"""
    try:
        scans = []
        for scan_id in scan_status:
            scan_info = {
                'scan_id': scan_id,
                'status': scan_status[scan_id]['status'],
                'start_time': scan_status[scan_id]['start_time'],
                'details': scan_details.get(scan_id, {})
            }
            scans.append(scan_info)

        return jsonify({
            'status': 'success',
            'scans': scans
        })

    except Exception as e:
        logger.exception("获取扫描列表时发生错误")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


###########################################################################
#####文件系统
###########################################################################

@app.route('/files', methods=['GET'])
def list_files():
    directory = os.path.abspath(os.path.join(os.getcwd(), 'output_reports'))  # 获取 output_reports 目录
    file_details = []

    try:
        # 遍历目录
        for root, dirs, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                relative_path = os.path.relpath(filepath, directory)  # 计算相对路径
                file_info = {
                    "name": filename,
                    "relative_path": relative_path,  # 添加相对路径
                    "size": os.path.getsize(filepath),
                    "created_time": time.ctime(os.path.getctime(filepath)),
                    "modified_time": time.ctime(os.path.getmtime(filepath))
                }
                file_details.append(file_info)

        return jsonify(file_details), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/download', methods=['GET'])
def download_file():
    filename = request.args.get('file')
    directory = os.path.abspath(os.path.join(os.getcwd(), 'output_reports'))
    return send_from_directory(directory, filename, as_attachment=True)


if __name__ == '__main__':
    import urllib3

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    app.run(host='0.0.0.0', port=8099, debug=True)
