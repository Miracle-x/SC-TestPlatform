<template>
  <el-container>
    <el-header>
      <h1>AttackAgent-大模型智能体漏洞利用模块</h1>
    </el-header>
    <el-main>
      <el-form :model="form" label-width="100px" style="display: flex;padding-right: 100px">
        <el-form-item label="目标URL" style="flex: 1;">
          <el-input v-model="form.url" placeholder="请输入要扫描的URL"></el-input>
        </el-form-item>
        <el-form-item label="漏洞编号" style="flex: 1;">
          <el-input v-model="form.cveID" placeholder="请输入要验证的漏洞编号"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="startScan" :disabled="isScanning">开始验证</el-button>
        </el-form-item>
      </el-form>
      <el-divider></el-divider>
      <!--      <div class="chat-container">-->
      <!--        <div-->
      <!--            v-for="(message, index) in messages"-->
      <!--            :key="index"-->
      <!--            :class="message.align === 'left' ? 'message-left' : 'message-right'"-->
      <!--        >-->
      <!--          <div class="name">-->
      <!--            <span>{{ message.name }} {{ message.time }} </span>-->
      <!--          </div>-->
      <!--          <div class="chat_message">-->
      <!--            {{ message.text }}-->
      <!--          </div>-->
      <!--        </div>-->
      <!--      </div>-->
      <el-card v-if="scanStatus" class="results-card">
        <h3>扫描结果（{{ scanStatus.details.status }}）</h3>
        <div class="results-window">
          <pre>{{ formattedResults }}</pre>
        </div>
      </el-card>
    </el-main>
  </el-container>
</template>

<script>
import {computed, ref} from 'vue';
import axios from 'axios';

export default {
  setup() {
    const form = ref({
      url: 'https://153.153.1.4:80',
      cveID: 'CVE-2016-7124'
    });
    const scanId = ref(null);
    const scanStatus = ref(null);
    const isScanning = ref(false);
    let pollingInterval = null;

    const startScan = async () => {
      try {
        isScanning.value = true;
        //   const response = await axios.get(`http://127.0.0.1:8099/scan?url=${form.value.url}`);
        //   scanId.value = response.data.scan_id;
        //
        //   // 开始轮询状态
        pollingInterval = setInterval(checkStatus, 2000);
      } catch (error) {
        console.error("启动扫描失败:", error);
        alert("启动扫描失败，请检查控制台");
        isScanning.value = false;
      }
    };

    let i = 1
    let result = ["\n    _   _   _             _           _                    _   \n   / \\ | |_| |_ __ _  ___| | __      / \\   __ _  ___ _ __ | |_ \n  / _ \\| __| __/ _` |/ __| |/ /____ / _ \\ / _` |/ _ \\ '_ \\| __|\n / ___ \\ |_| || (_| | (__|   <_____/ ___ \\ (_| |  __/ | | | |_ \n/_/   \\_\\__|\\__\\__,_|\\___|_|\\_\\   /_/   \\_\\__, |\\___|_| |_|\\__|\n                                          |___/      \n[*] Attack-Agent v1.3.2\n[*] Checking URL: https://153.153.1.4:80\n[*] Target CVE: CVE-2016-7124", '[+] Sending request...\n[+] Response received: 200 OK', '[*] Analyzing response...\n[+] Checking for CVE indicators...', '[!] CVE-2016-7124 found in the response!\n    - Vulnerable component: ExampleService v2.1.0\n    - Affected files: /path/to/affected/file.php\n    - More info: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-7124', '[*] Detailed Analysis:\n    - Response Headers:\n      - Content-Type: text/html; charset=UTF-8\n      - Server: ExampleServer v1.0\n      - X-Powered-By: ExampleFramework\n    - Response Time: 120ms', '[+] Searching for exploit patterns...\n[!] Exploit patterns matched:\n    - SQL Injection vulnerability in input validation', '[*] Attempting to retrieve sensitive data...\n[+] Sensitive data retrieval successful!\n    - User data exposed: example_user\n    - Password hash: $2y$10$abcdefghijklmnopqrstuv', '[*] Checking for additional CVEs...\n[+] No additional CVEs found.', '[*] Summary:\n    - Target URL: https://153.153.1.4:80\n    - CVE Status: Vulnerable\n    - Timestamp: 2024-11-10 12:00:00 UTC\n    - Affected Components: ExampleService v2.1.0', '[*] Recommendations:\n    - Upgrade ExampleService to v2.2.0 or later.\n    - Implement input validation and sanitization.\n    - Conduct a full security audit.', '[*] Logging results...\n[+] Results logged to: /var/log/cve-checker/results.log', '[*] Finished scanning.', '[*] Starting new scan...\n[*] Checking URL: https://153.153.1.4:80\n[*] Target CVE: CVE-2016-7124', '[+] Sending request...\n[+] Response received: 200 OK', '[*] Analyzing response...\n[+] Checking for CVE indicators...\n[!] CVE-2016-7124 found in the response!\n    - Vulnerable component: ExampleService v2.1.0\n    - More info: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-7124', '[*] Response Headers:\n    - Content-Length: 1024\n    - Last-Modified: Fri, 01 Jan 2023 00:00:00 GMT', '[*] Checking for active exploits...\n[+] Active exploits detected in environment.', '[*] Attempting to exploit...\n[!] Exploit successful! Access granted.\n    - Shell access obtained.', '[*] Gathering system information...\n[+] OS Version: Linux 5.4.0-26-generic\n[+] Kernel Version: 5.4.0\n[+] CPU Info: Intel(R) Xeon(R) CPU E5-2670 v2 @ 2.50GHz', '[*] Searching for user accounts...\n[+] User accounts found:\n    - admin\n    - guest\n    - user1', '[*] Extracting user account details...\n[+] User details retrieved:\n    - admin: admin@example.com\n    - guest: guest@example.com', '[*] Checking for password policies...\n[+] No strong password policies detected.', '[*] Checking for outdated packages...\n[+] Outdated packages found:\n    - ExamplePackage v1.0.0 (update available)\n    - AnotherPackage v1.5.1 (update available)', '[*] Recommendations:\n    - Update all outdated packages.\n    - Enforce strong password policies.\n    - Regularly audit user accounts.', '[*] Log summary of findings...\n[+] Log saved to /var/log/cve-checker/summary.log', '[*] Scan complete.\n[*] Starting new scan...\n[*] Checking URL: https://153.153.1.4:80\n[*] Target CVE: CVE-2016-7124', '[+] Sending request...\n[+] Response received: 200 OK', '[*] Analyzing response...\n[+] Checking for CVE indicators...\n[!] CVE-2016-7124 confirmed in the response!', '[+] Response Time: 115ms\n[+] Content Length: 2048 bytes', '[*] Searching for related vulnerabilities...\n[+] No related vulnerabilities found.', '[*] Summary of findings:\n    - Vulnerable Component: ExampleService v2.1.0\n    - CVE Status: Vulnerable\n    - Recommendations logged.', '[*] Finished scanning.', '[*] Checking network configuration...\n[+] Open Ports:\n    - 80: HTTP\n    - 443: HTTPS', '[*] Checking firewall rules...\n[+] Firewall status: Active', '[*] Generating final report...\n[+] Report generated at: /var/log/cve-checker/final_report_2024-11-10.txt', '[*] All scans completed successfully.']
    const checkStatus = async () => {
      try {
        // const response = await axios.get(`http://127.0.0.1:8099/scan/status/${scanId.value}`);
        scanStatus.value = {
          'scan_id': 'scan_id',
          'status': 'running',
          'details': {'status': 'running'},
          'current_results': result.slice(Math.max(i - 100, 0), i),
          'total_results_count': result.length
        }

        console.log(scanStatus)
        // 如果扫描完成，停止轮询
        if (i === result.length) {
          clearInterval(pollingInterval);
          isScanning.value = false;
        }
        i += 1
      } catch (error) {
        console.error("获取扫描状态失败:", error);
        alert("获取扫描状态失败，请检查控制台");
        clearInterval(pollingInterval);
        isScanning.value = false;
      }
    };

    const formattedResults = computed(() => {
      return scanStatus.value?.current_results.join('\n\n') || '';
    });
    const messages = [
      {text: "你好！", align: "left", name: "王阳阳", time: "18:07"},
      {text: "你好！", align: "right", name: "丽丝", time: "19:21"},
      {text: "如何才能帮助您？", align: "left", name: "王阳阳", time: "21:26"},
      {
        text: "我需要帮助进行Vue.js开发我需要帮助进行Vue.js开发我需要帮助进行Vue.js开发我需要帮助进行Vue.js开发",
        align: "right",
        name: "丽丝",
        time: "22:37"
      }]


    return {
      form,
      scanId,
      scanStatus,
      isScanning,
      startScan,
      checkStatus,
      formattedResults,
      messages
    };
  }
};
</script>


<style scoped>
h1 {
  text-align: center;
  margin-bottom: 20px;
}

.chat-container {
  overflow: hidden;
  display: flex;
  flex-direction: column;
  width: 600px;
  background: #ffffff;
  border: 1px solid #e4e7ed;
  border-radius: 3px;
  padding: 16px;

  .name {
    font-family: PingFangSC-Regular;
    font-weight: 400;
    font-size: 12px;
    color: #909399;
    margin-bottom: 6px;
  }
}

.chat_message {
  padding: 6px 12px;
  background: #f8f8f9;
  border-radius: 4px;
  margin-bottom: 15px;
  word-wrap: break-word;
  font-weight: 400;
  font-size: 14px;
  color: #303133;
}

.message-left {
  max-width: 418px;
  align-self: flex-start;

  .chat_message {
    background-color: #f8f8f9;
  }

  .name {
    align-self: flex-start;
  }
}

.message-right {
  max-width: 418px;
  align-self: flex-end;
  display: flex;
  flex-direction: column;

  .chat_message {
    background-color: #ebf3ff;
  }

  .name {
    align-self: flex-end;
  }
}


.results-card {
  margin-top: 20px;
}

.results-window {
  background-color: #1e1e1e; /* 控制台背景色 */
  color: #ffffff; /* 字体颜色 */
  padding: 10px;
  border-radius: 5px;
  max-height: 500px; /* 限制高度 */
  overflow-y: auto; /* 允许垂直滚动 */
  font-family: monospace; /* 使用等宽字体 */
}
</style>