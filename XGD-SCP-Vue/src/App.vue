<template>
  <div id="app">
    <el-menu
        :default-active="activeIndex"
        class="el-menu-demo"
        mode="horizontal"
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b"
        @select="handleSelect"
    >
      <el-sub-menu index="1">
        <template #title>靶场环境</template>
        <el-menu-item index="1-1" @click="navigateTo('/environment')">环境设置</el-menu-item>
        <el-menu-item index="1-2" @click="navigateTo('/deepflow')">数据监控</el-menu-item>
      </el-sub-menu>
      <el-sub-menu index="2">
        <template #title>安全工具</template>
        <el-menu-item index="2-1" @click="navigateTo('/nessus')">Nessus</el-menu-item>
        <el-menu-item index="2-2" @click="navigateTo('/cn-nuclei')">CN-Nuclei</el-menu-item>
        <el-menu-item index="2-3" @click="navigateTo('/attack-agent')">AttackAgent</el-menu-item>
      </el-sub-menu>
      <el-menu-item index="3" @click="navigateTo('/report')">报告生成</el-menu-item>
    </el-menu>
    <RouterView/>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const navigateTo = (path) => {
  router.push(path)
}
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
}

#app {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.el-menu {
  flex-shrink: 0;
}

.iframe-container {
  flex: 1;
  overflow: hidden;
}

iframe {
  width: 100%;
  height: 100%;
  border: none;
}
</style>