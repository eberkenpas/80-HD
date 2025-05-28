#!/usr/bin/env python3
import os
import sys
import time
import logging
import netifaces
import importlib
import threading
import subprocess
import socketserver
from find_device import get_cpu_serial_number
import ros_robot_controller_sdk as rrc

# 获取当前脚本所在路径
path = os.path.split(os.path.realpath(__file__))[0]
log_file_path = os.path.join(path, "wifi.log")

# 创建日志文件（如果不存在）
if not os.path.exists(log_file_path):
    os.system(f'touch {log_file_path}')

# 配置文件路径
config_file_name = "wifi_conf.py"
internal_config_file_dir_path = "/etc/wifi"
external_config_file_dir_path = path
internal_config_file_path = os.path.join(internal_config_file_dir_path, config_file_name)
external_config_file_path = os.path.join(external_config_file_dir_path, config_file_name)

# 全局变量
ros_control_enabled = False
current_wifi_mode = None  # 用于记录当前的网络模式
server = None  # 全局服务器实例
ip = None  # 当前IP地址

# 初始化Board实例
board = rrc.Board()

# 配置日志记录
logger = logging.getLogger("WiFi工具")
logger.setLevel(logging.DEBUG)
log_handler = logging.FileHandler(log_file_path)
log_handler.setLevel(logging.INFO)
log_formatter = logging.Formatter('%(name)s - %(asctime)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)

def update_globals(module):
    """
    动态导入或重新加载模块，并将模块中的变量更新到全局命名空间。
    """
    if module in sys.modules:
        mdl = importlib.reload(sys.modules[module])
    else:
        mdl = importlib.import_module(module)
    if "__all__" in mdl.__dict__:
        names = mdl.__dict__["__all__"]
    else:
        names = [x for x in mdl.__dict__ if not x.startswith("_")]
    globals().update({k: getattr(mdl, k) for k in names})

def get_wifi_ip():
    """
    获取当前连接的WiFi接口的IP地址。
    """
    interfaces = netifaces.interfaces()

    for interface in interfaces:
        if interface.startswith('wlan'):
            addresses = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addresses:
                ip_info = addresses[netifaces.AF_INET][0]
                ip_address = ip_info['addr']
                return ip_address

    return None

def reset_wifi():
    """
    重置WiFi配置并重启WiFi服务。
    """
    os.system("sudo rm /etc/wifi/* -rf > /dev/null 2>&1")
    os.system("sudo systemctl restart wifi.service > /dev/null 2>&1")
    logger.info("WiFi已重置并重启服务。")

class TCPHandler(socketserver.BaseRequestHandler):
    """
    TCP请求处理类，用于接收命令并执行相应操作。
    """
    def handle(self):
        self.request.settimeout(2)
        data = b""
        while True:
            try:
                chunk = self.request.recv(1024)
                if not chunk:
                    break
                data += chunk
                if data.strip() == b"resetwifi":
                    logger.info("收到重置WiFi命令。")
                    reset_wifi()
                    break
            except socket.timeout:
                logger.warning('TCP连接超时。')
                break
            except Exception as e:
                logger.error(f"TCP处理时出错: {e}")
                break
        self.request.close()

class PhoneServer(socketserver.TCPServer):
    """
    定制的TCP服务器类。
    """
    def __init__(self, server_address, RequestHandlerClass):
        super().__init__(server_address, RequestHandlerClass)

    def handle_timeout(self):
        logger.warning('TCP服务器超时。')

def start_server(ip, port):
    """
    启动TCP服务器。
    """
    server = PhoneServer((ip, port), TCPHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    logger.info(f"TCP服务器已启动在 {ip}:{port}")
    return server

def stop_server(server):
    """
    停止TCP服务器。
    """
    if server:
        server.shutdown()
        server.server_close()
        logger.info("TCP服务器已停止。")
    return None

def check_ros2_control():
    """
    检查ROS2控制节点是否存在，以决定LED控制方式。
    """
    global ros_control_enabled
    try:
        process = subprocess.Popen(
            ["docker", "exec", '-u', 'ubuntu', '-w', '/home/ubuntu', 'MentorPi', 
             '/bin/zsh', '-c', 'source /home/ubuntu/.zshrc && ros2 topic list'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate(timeout=5)  # 设置超时为5秒
        topics = stdout.decode().split('\n')
        if '/ros_robot_controller/set_led' in topics:
            ros_control_enabled = True
            logger.info("检测到ROS控制节点，启用ROS控制LED。")
        else:
            ros_control_enabled = False
            logger.info("未检测到ROS控制节点，使用本地控制LED。")
    except subprocess.TimeoutExpired:
        process.kill()
        ros_control_enabled = False
        logger.warning("检测ROS2控制超时，使用本地控制LED。")
    except Exception as e:
        ros_control_enabled = False
        logger.error(f"检测ROS2节点时出错: {e}")

def set_led(led_id, on_time, off_time, repeat=0):
    """
    设置LED状态，根据ROS控制是否启用，选择不同的控制方式。
    """
    if ros_control_enabled:
        ros_command = f"ros2 topic pub /ros_robot_controller/set_led ros_robot_controller_msgs/msg/LedState '{{id: {led_id}, on_time: {on_time}, off_time: {off_time}, repeat: {repeat}}}' --once"
        full_command = [
            'docker', 'exec', '-u', 'ubuntu', '-w', '/home/ubuntu', 'MentorPi',
            '/bin/zsh', '-c', f"source /home/ubuntu/.zshrc && {ros_command}"
        ]
        logger.info(f"执行ROS命令: {' '.join(full_command)}")
        result = subprocess.run(full_command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode != 0:
            logger.error(f"发布ROS 2消息时出错: {result.stderr.decode('utf-8')}")
    else:
        try:
            board.set_led(on_time, off_time, repeat=repeat, led_id=led_id)
            logger.info(f"使用rrc.Board本地控制LED: id={led_id}, on_time={on_time}, off_time={off_time}, repeat={repeat}")
        except Exception as e:
            logger.error(f"本地控制LED时出错: {e}")

def get_connect():
    """
    获取当前连接的WiFi名称。
    """
    try:
        result = subprocess.run(['nmcli', '-t', 'con', 'show', '--active'], stdout=subprocess.PIPE)
        active_conns = result.stdout.decode().split('\n')
        for conn in active_conns:
            if conn:
                conn_details = conn.split(':')
                if len(conn_details) >= 3 and 'wireless' in conn_details[2]:
                    wifi = conn_details[0]
                    return wifi
    except Exception as e:
        logger.error(f"获取WiFi连接时出错: {e}")
    return None

def disconnect():
    """
    断开当前WiFi连接。
    """
    try:
        wifi = get_connect()
        if wifi:
            os.system(f'nmcli connection down {wifi}')
            os.system(f'nmcli connection delete {wifi}')
            os.system('rm /etc/NetworkManager/system-connections/*')
            logger.info(f"已断开并删除WiFi连接: {wifi}")
    except Exception as e:
        logger.error(f"断开WiFi连接时出错: {e}")

def setup_ap_mode():
    """
    切换到AP模式的具体实现。
    """
    global current_wifi_mode, ip, server

    current_wifi_mode = 1
    set_led(1, 1, 0, 1)  # LED1常亮
    set_led(2, 0.5, 0.5, 0)  # LED2闪烁

    disconnect()

    # 配置AP模式
    try:
        os.system(f'nmcli con add type wifi ifname wlan0 con-name {WIFI_AP_SSID} autoconnect yes ssid {WIFI_AP_SSID}')
        os.system(f'nmcli con modify {WIFI_AP_SSID} 802-11-wireless.mode ap ipv4.method shared')
        os.system(f'nmcli con modify {WIFI_AP_SSID} wifi-sec.key-mgmt wpa-psk wifi-sec.psk {WIFI_AP_PASSWORD}')
        os.system(f'nmcli con modify {WIFI_AP_SSID} wifi.band {WIFI_FREQ_BAND} wifi.channel {WIFI_CHANNEL}')
        os.system(f'nmcli con modify {WIFI_AP_SSID} ipv4.addresses {WIFI_AP_GATEWAY}/24')
        logger.info(f"配置AP模式: SSID={WIFI_AP_SSID}, 密码={WIFI_AP_PASSWORD}, 频段={WIFI_FREQ_BAND}, 频道={WIFI_CHANNEL}")

        # 等待AP模式生效
        timeout = 0
        while True:
            timeout += 1
            wifi = get_connect()
            if wifi == WIFI_AP_SSID:
                logger.info(f"AP创建成功: {WIFI_AP_SSID}")
                ip = WIFI_AP_GATEWAY
                server = start_server(ip, 9028)
                break
            if timeout == 20:
                logger.warning("重启NetworkManager...")
                os.system('systemctl restart NetworkManager')
            if timeout > 20:
                logger.error("无法创建AP，重启系统...")
                os.system('reboot')
                break
            time.sleep(1)
    except Exception as e:
        logger.error(f"设置AP模式时出错: {e}")

def setup_client_mode():
    """
    切换到客户端模式的具体实现。
    """
    global current_wifi_mode, ip, server

    current_wifi_mode = 2
    set_led(1, 1, 0, 1)  # LED1常亮
    set_led(2, 0.05, 0.05, 0)  # LED2 50ms闪烁

    disconnect()

    retry_count = 0
    max_retries = 3

    # 尝试连接客户端模式三次
    while retry_count < max_retries:
        try:
            p = subprocess.Popen(['nmcli', 'device', 'wifi', 'connect', WIFI_STA_SSID, 'password', WIFI_STA_PASSWORD], 
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = p.communicate(timeout=10)  # 设置超时为10秒
            if p.returncode == 0:
                logger.info(f"成功连接到WiFi: {WIFI_STA_SSID}")
                break
            else:
                retry_count += 1
                logger.warning(f"连接到WiFi失败: {stderr.decode('utf-8')}. 重试 {retry_count}/{max_retries}")
                time.sleep(2)
        except subprocess.TimeoutExpired:
            p.kill()
            retry_count += 1
            logger.warning(f"连接到WiFi超时。重试 {retry_count}/{max_retries}")
        except Exception as e:
            p.kill()
            retry_count += 1
            logger.error(f"连接到WiFi时出错: {e}. 重试 {retry_count}/{max_retries}")

    if retry_count >= max_retries:
        logger.error(f"无法连接到SSID: {WIFI_STA_SSID}，切换到AP模式。")
        # 删除 /etc/wifi/* 文件
        try:
            os.system("sudo rm /etc/wifi/* -rf > /dev/null 2>&1")
            logger.info("已删除 /etc/wifi/* 文件。")
        except Exception as e:
            logger.error(f"删除 /etc/wifi/* 文件时出错: {e}")
        # 切换到AP模式
        setup_ap_mode()
        return

    # 检查是否成功连接并获取IP
    timeout = 0
    while True:
        ssid_name = get_connect()
        if ssid_name == WIFI_STA_SSID:
            logger.info(f"已连接到 {WIFI_STA_SSID}")
            set_led(1, 1, 0, 1)  # LED1常亮
            set_led(2, 1, 0, 1)  # LED2常亮，表示成功连接

            # 获取IP地址
            while True:
                wifi_ip = get_wifi_ip()
                if wifi_ip:
                    if wifi_ip != ip:
                        ip = wifi_ip
                        if server:
                            server = stop_server(server)
                        server = start_server(ip, 9028)
                    break
                time.sleep(1)
            break
        else:
            if timeout >= WIFI_TIMEOUT:
                logger.error(f"无法连接到SSID: {WIFI_STA_SSID}，切换到AP模式。")
                # 删除 /etc/wifi/* 文件
                try:
                    os.system("sudo rm /etc/wifi/* -rf > /dev/null 2>&1")
                    logger.info("已删除 /etc/wifi/* 文件。")
                except Exception as e:
                    logger.error(f"删除 /etc/wifi/* 文件时出错: {e}")
                # 切换到AP模式
                setup_ap_mode()
                break
            timeout += 1
            time.sleep(1)

def WIFI_MGR():
    """
    管理WiFi连接的主逻辑，根据WIFI_MODE进行模式切换。
    """
    global WIFI_AP_SSID, WIFI_STA_SSID, WIFI_AP_PASSWORD, WIFI_STA_PASSWORD
    global server, ip, current_wifi_mode

    check_ros2_control()  # 在WiFi管理器启动时检查ROS控制

    if WIFI_MODE == 1:  # AP模式
        setup_ap_mode()
    elif WIFI_MODE == 2:  # 客户端模式
        setup_client_mode()
    else:
        logger.error("无效的WIFI_MODE")
        set_led(1, 1, 0, 1)  # LED1常亮
        set_led(2, 0.5, 0.5, 0)  # LED2闪烁，表示错误

def monitor_ros_node():
    """
    监控ROS节点的线程函数，动态调整LED状态。
    """
    global ros_control_enabled
    global current_wifi_mode
    ros_was_enabled = False  # 记录上一次的ROS控制状态

    while True:
        check_ros2_control()

        if ros_control_enabled:
            if not ros_was_enabled:
                logger.info("检测到ROS控制，发送LED指令...")
                if current_wifi_mode == 1:
                    set_led(1, 1, 0, 1)  # AP模式: LED1常亮
                    set_led(2, 0.5, 0.5, 0)  # AP模式: LED2闪烁
                elif current_wifi_mode == 2:
                    wifi_connected = get_connect()
                    if wifi_connected:
                        set_led(1, 1, 0, 1)  # 客户端模式: LED1常亮
                        set_led(2, 1, 0, 1)  # 客户端模式: LED2常亮
                    else:
                        set_led(1, 1, 0, 1)  # 客户端模式: LED1常亮
                        set_led(2, 0.05, 0.05, 0)  # 客户端模式: LED2闪烁
                ros_was_enabled = True  # 更新为ROS控制启用状态
        else:
            if ros_was_enabled:
                logger.info("ROS控制丢失，保持当前LED状态...")
                ros_was_enabled = False  # 更新状态标志

        time.sleep(5)  # 每5秒检查一次

if __name__ == "__main__":
    # 配置参数
    ap_prefix = 'HW-'
    sn = get_cpu_serial_number()   # 获取CPU序列号
    WIFI_MODE = 2  # 1表示AP模式，2表示客户端模式，3表示AP模式并共享eth0的互联网
    WIFI_AP_SSID = ''.join([ap_prefix, sn[0:8]])
    WIFI_STA_SSID = "ssid"  # 请替换为目标WiFi名称
    WIFI_AP_PASSWORD = "hiwonder"  # 请替换为AP模式的密码
    WIFI_STA_PASSWORD = "12345678"  # 请替换为客户端模式的密码
    WIFI_AP_GATEWAY = "192.168.149.1"
    WIFI_CHANNEL = 36
    WIFI_FREQ_BAND = 'a'  # 'a'表示5G, 'g'表示2.4G
    WIFI_TIMEOUT = 30  # 客户端模式下的连接超时时间（秒）
    WIFI_LED = True
    ip = WIFI_AP_GATEWAY

    # 读取配置文件
    if os.path.exists(config_file_name):
        update_globals(os.path.splitext(config_file_name)[0])
    if os.path.exists(internal_config_file_path):
        sys.path.insert(0, internal_config_file_dir_path)
        update_globals(os.path.splitext(config_file_name)[0])
    if os.path.exists(external_config_file_path):
        sys.path.insert(1, external_config_file_dir_path)
        update_globals(os.path.splitext(config_file_name)[0])

    # 启动WiFi管理线程
    if WIFI_LED:
        wifi_thread = threading.Thread(target=WIFI_MGR)
        wifi_thread.start()

    # 启动ROS节点监控线程
    node_monitor_thread = threading.Thread(target=monitor_ros_node)
    node_monitor_thread.start()

    # 等待线程结束
    wifi_thread.join()
    node_monitor_thread.join()
