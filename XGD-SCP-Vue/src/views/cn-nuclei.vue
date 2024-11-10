<template>
  <el-container>
    <el-header>
      <h1>CN-Nuclei漏洞扫描模块</h1>
    </el-header>
    <el-main>
      <el-form :model="form" label-width="100px" style="display: flex; padding-right: 100px">
        <el-form-item label="目标URL" style="flex: 1;">
          <el-input v-model="form.url" placeholder="请输入要扫描的URL"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="startScan" :disabled="isScanning">开始扫描</el-button>
        </el-form-item>
      </el-form>
      <el-divider></el-divider>

      <!-- 扫描状态展示 -->
<!--      <el-card v-if="scanStatus">-->
<!--        <h3>扫描状态</h3>-->
<!--        <p><strong>状态:</strong> </p>-->
<!--        <p><strong>严重性:</strong> {{ scanStatus.details.severity }}</p>-->
<!--        <p><strong>开始时间:</strong> {{ scanStatus.details.start_time }}</p>-->
<!--        <p><strong>目标URL:</strong> {{ scanStatus.details.target_url }}</p>-->
<!--        <p><strong>结果数量:</strong> {{ scanStatus.total_results_count }}</p>-->
<!--      </el-card>-->

      <!-- 结果展示 -->
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
import { ref, computed } from 'vue';
import axios from 'axios';

export default {
  setup() {
    const form = ref({
      url: 'https://153.153.1.4:80'
    });
    const scanId = ref(null);
    const scanStatus = ref(null);
    const isScanning = ref(false);
    let pollingInterval = null;

    const startScan = async () => {
      try {
        isScanning.value = true;
        const response = await axios.get(`http://127.0.0.1:8099/scan?url=${form.value.url}`);
        scanId.value = response.data.scan_id;

        // 开始轮询状态
        pollingInterval = setInterval(checkStatus, 2000);
      } catch (error) {
        console.error("启动扫描失败:", error);
        alert("启动扫描失败，请检查控制台");
        isScanning.value = false;
      }
    };

    const checkStatus = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8099/scan/status/${scanId.value}`);
        scanStatus.value = response.data;

        // 如果扫描完成，停止轮询
        if (response.data.status !== 'running') {
          clearInterval(pollingInterval);
          isScanning.value = false;
        }
      } catch (error) {
        console.error("获取扫描状态失败:", error);
        alert("获取扫描状态失败，请检查控制台");
        clearInterval(pollingInterval);
        isScanning.value = false;
      }
    };

    const formattedResults = computed(() => {
      return scanStatus.value?.current_results.join('\n') || '';
    });

    return {
      form,
      scanId,
      scanStatus,
      isScanning,
      startScan,
      checkStatus,
      formattedResults
    };
  }
};
</script>

<style scoped>
h1 {
  text-align: center;
  margin-bottom: 20px;
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