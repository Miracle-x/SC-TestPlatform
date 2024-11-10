<template>
  <el-container>
    <el-header>
      <h1>Nessus-资产发现模块</h1>
    </el-header>
    <el-main>
      <el-form :model="form" label-width="100px" style="display: flex; padding-right: 100px">
        <el-form-item label="子网网段" style="flex: 1;">
          <el-input v-model="form.url" placeholder="请输入要扫描的子网网段，如153.153.1.0/24"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="discoverHosts" :disabled="isScanning">扫描资产</el-button>
        </el-form-item>
      </el-form>
      <el-divider></el-divider>
      <el-card v-if="scanStatus">
        <h3>扫描状态: {{ scanStatus }}</h3>
      </el-card>
      <el-table v-if="hosts.length" :data="hosts" style="width: 100%">
        <el-table-column prop="hostname" label="主机名"></el-table-column>
        <el-table-column prop="ip" label="IP地址"></el-table-column>
        <el-table-column label="开放端口">
          <template v-slot="scope">
            <div>
              <el-tag
                  v-for="port in scope.row.ports"
                  :key="port.port"
                  style="margin-right: 5px"
              >
                {{ port.port }} ({{ port.protocol }})
              </el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="btn" label="选项" width="100px">
          <el-button type="primary" @click="navigateTo('/cn-nuclei')">扫描漏洞</el-button>
        </el-table-column>
      </el-table>
      <div v-if="hosts.length"
           style="width: 100%;height: 300px;display: flex;align-items: center;justify-content: center">

      </div>
    </el-main>
  </el-container>
</template>

<script>
import axios from 'axios';
import {ref} from 'vue';
import router from "@/router/index.js";


const navigateTo = (path) => {
  router.push(path)
}

export default {
  setup() {
    const form = ref({
      url: '153.153.1.0/24'
    });
    const isScanning = ref(false);
    const scanStatus = ref('');
    const hosts = ref([]);

    const discoverHosts = async () => {
      isScanning.value = true;
      scanStatus.value = '';
      hosts.value = [];
      const templateUuid = 'YOUR_TEMPLATE_UUID'; // Replace with actual template UUID
      const policyId = 'YOUR_POLICY_ID'; // Replace with actual policy ID
      const scannerId = 'YOUR_SCANNER_ID'; // Replace with actual scanner ID

      const scanPayload = {
        uuid: templateUuid,
        settings: {
          name: `Scan of ${form.value.url}`,
          description: `Scanning subnet: ${form.value.url}`,
          enabled: true,
          launch: 'ON_DEMAND',
          text_targets: form.value.url,
          policy_id: policyId,
          scanner_id: scannerId,
          agent_group_id: []
        }
      };

      const accessKey = 'a847fe1953b09c03e88d2746db18062d8420bc533ff0ba7ac361a42955bf126a';
      const secretKey = '37098ec5f9d7be9865bd743a717b75887e13bbfc91a17fb3579ceffadd1cbaed';
      const nessusUrl = '/api/scans'; // 使用代理路径

      const header = {
        'X-ApiKeys': `accessKey=${accessKey}; secretKey=${secretKey}`,
        'Content-Type': 'application/json',
        'Accept': 'text/plain'
      };

      try {
        // const response = await axios.post(nessusUrl, scanPayload, {headers: header});
        // const scanId = response.data.scan.id; // Get the scan ID from the response
        // scanStatus.value = '扫描已启动，正在处理...';
        //
        // // Polling for scan results
        // await getScanResults(scanId);


        scanStatus.value = '扫描已启动，正在处理...';
        await getScanResults(1);
      } catch (error) {
        console.error('启动扫描失败:', error.response ? error.response.data : error.message);
        scanStatus.value = '启动扫描失败';
      } finally {
        isScanning.value = false;
      }
    };

    // const getScanResults = async (scanId) => {
    //   const accessKey = 'a847fe1953b09c03e88d2746db18062d8420bc533ff0ba7ac361a42955bf126a';
    //   const secretKey = '37098ec5f9d7be9865bd743a717b75887e13bbfc91a17fb3579ceffadd1cbaed';
    //   const nessusUrl = `/api/scans/${scanId}/results`; // 使用代理路径
    //
    //   const header = {
    //     'X-ApiKeys': `accessKey=${accessKey}; secretKey=${secretKey}`,
    //     'Content-Type': 'application/json',
    //     'Accept': 'text/plain'
    //   };
    //
    //   try {
    //     const response = await axios.get(nessusUrl, {headers: header});
    //     hosts.value = response.data.hosts; // 假设返回的数据结构中有 hosts 字段
    //     scanStatus.value = '扫描完成';
    //   } catch (error) {
    //     console.error('获取扫描结果失败:', error.response ? error.response.data : error.message);
    //   }
    // };

    //
    //
    const getScanResults = async (scanId) => {
      // 示例数据
      const sampleHosts = [
        {
          hostname: 'busybox1',
          ip: '153.153.1.2',
          ports: [
            {port: 22, protocol: 'tcp'},
          ]
        },
        {
          hostname: 'busybox2',
          ip: '153.153.1.3',
          ports: [
            {port: 22, protocol: 'tcp'},
          ]
        },
        {
          hostname: 'php',
          ip: '153.153.1.4',
          ports: [
            {port: 80, protocol: 'tcp'},
          ]
        },
        {
          hostname: 'mariadb',
          ip: '153.153.1.5',
          ports: [
            {port: 3306, protocol: 'tcp'}
          ]
        }
      ];

      // 将示例数据赋值给 hosts
      setTimeout(() => {
        hosts.value = sampleHosts      // 直接使用示例数据
        scanStatus.value = '扫描完成'; // 更新扫描状态
      }, 3000)
    };
    //
    //

    return {
      form,
      isScanning,
      scanStatus,
      hosts,
      discoverHosts,
      navigateTo
    };
  }
};
</script>

<style scoped>
h1 {
  text-align: center;
  margin-bottom: 20px;
}
</style>