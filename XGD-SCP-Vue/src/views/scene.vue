<template>
  <div style="padding: 30px 30px 0 0;display: flex; justify-content: end">
    <el-button type="primary" class="ml-2">新增场景</el-button>
  </div>
  <el-container style="padding: 30px">
    <el-row :gutter="20">
      <el-col v-for="(scene, index) in scenes" :key="index" :span="8">
        <el-card class="card">
          <template #header>
            <h3>场景{{ index + 1 }}：{{ scene.name }}</h3>
          </template>
          <div class="card-content">
            <img :src="scene.image" alt="Scene Image" class="card-image"/>
            <p>子网网段: {{ scene.subnet }}</p>
            <p>节点:</p>
            <ul>
              <li v-for="node in scene.nodes" :key="node.name">
                {{ node.name }}: {{ node.ip }}
              </li>
            </ul>
          </div>
          <template #footer>
            <div style="display: flex;justify-content: space-between">
              <el-input v-if="scene.type === 'ipRequire'" v-model="ipInput[index]" placeholder="输入防火墙IP"
                        style="padding-right: 30px"/>
              <div></div>
              <el-button type="primary" @click="startScene(scene.namespace)">开启场景</el-button>
            </div>
          </template>
        </el-card>
      </el-col>

    </el-row>
  </el-container>
</template>

<script>
// 定义要使用的 namespace
import axios from "axios";

// 请求 /deploy 接口
const deployNamespace = async (namespace) => {
  try {
    const response = await axios.post('http://localhost:8099/deploy', {
      namespace: namespace
    });
    console.log('Deploy Response:', response.data);
    return response.data
  } catch (error) {
    console.error('Error deploying namespace:', error.response.data);
    return false
  }
};

// 请求 /namespace/<namespace> 接口
const checkNamespace = async (namespace) => {
  try {
    const response = await axios.get(`http://localhost:8099/namespace/${namespace}`);
    console.log('Check Namespace Response:', response.data);
    return response.data.exists
  } catch (error) {
    console.error('Error checking namespace:', error.response.data);
    return false
  }
};

console.log(
    await checkNamespace('net1')
)

const navigateTo = (path) => {
  router.push(path)
}

import waibu from '@/assets/waibu.png';
import neibu from '@/assets/neibu.png';
import router from "@/router/index.js";

export default {
  data() {
    return {
      ipInput: [],
      scenes: [
        {
          name: '虚拟内网(net1)',
          namespace: 'net1',
          subnet: '153.153.1.0/24',
          nodes: [
            {name: 'PC节点1', ip: '153.153.1.2'},
            {name: 'PC节点2', ip: '153.153.1.3'},
            {name: 'PC节点3', ip: '153.153.1.4'},
            {name: '数据库节点1', ip: '153.153.1.5'}
          ],
          image: neibu,
        },
        {
          name: '虚拟内网(net2)，接入真实防火墙设备',
          namespace: 'net2',
          subnet: '153.153.2.0/24',
          nodes: [
            {name: 'PC节点1', ip: '153.153.2.2'},
            {name: 'PC节点2', ip: '153.153.2.3'},
            {name: 'PC节点3', ip: '153.153.2.4'},
            {name: '数据库节点1', ip: '153.153.2.5'}
          ],
          image: waibu,
          type: 'ipRequire',
        }
      ],
    };
  },
  methods: {
    async startScene(sceneName) {
      let res = await deployNamespace(sceneName)
      console.log(res)
      if(res.status){
        navigateTo('/environment')
      }
    },
  },
};
</script>

<style scoped>

.card-image {
  width: 100%;
  height: auto;
}

.card-content {
  height: 500px !important;
  overflow: auto;
}
</style>