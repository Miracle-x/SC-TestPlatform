<template>
  <el-menu
      :default-active="activeIndex"
      class="el-menu-demo"
      mode="horizontal"
      background-color="#545c64"
      text-color="#fff"
      active-text-color="#ffd04b"
      :ellipsis="false"
      @select="handleSelect"
  >
    <el-menu-item index="0" style="width: 30%;display: flex;justify-content: start">
      <img
          style="width: 200px"
          src="./assets/logo2024.png"
          alt="Element logo"
      />
      <span style="font-size: 20px;margin-left: 30px">网络安全靶场平台</span>
    </el-menu-item>
    <div class="flex-grow"/>
    <el-sub-menu index="1">
      <template #title>靶场环境</template>
      <el-menu-item index="1-1" @click="navigateTo('/scene')">场景管理</el-menu-item>
      <el-menu-item index="1-2" @click="navigateTo('/environment')">资源管理</el-menu-item>
      <el-menu-item index="1-3" @click="navigateTo('/deepflow')">流量监控</el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="2">
      <template #title>安全工具</template>
      <el-menu-item index="2-1" @click="navigateTo('/nessus')">Nessus</el-menu-item>
      <el-menu-item index="2-2" @click="navigateTo('/cn-nuclei')">CN-Nuclei</el-menu-item>
      <el-menu-item index="2-3" @click="navigateTo('/attack-agent')">AttackAgent</el-menu-item>
    </el-sub-menu>
    <el-menu-item index="3" @click="navigateTo('/report')">报告生成</el-menu-item>

    <div class="flex-grow"/>
    <div class="block" style="display: flex;align-items: center;justify-content: end;margin-right: 50px; width: 30%;">
      <el-avatar :size="50" :src="circleUrl"/>
    </div>
  </el-menu>
  <RouterView></RouterView>
</template>

<script setup>
import {useRouter} from 'vue-router'

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

.flex-grow {
  flex-grow: 1;
}
</style>