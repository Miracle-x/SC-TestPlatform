<template>
  <el-container style="width: 100%; height: 100%">
    <el-header style="width: 100%;">
      <h1>报告列表</h1>
    </el-header>
    <el-main>
      <el-table
        :data="files"
        :row-key="row => row.name"
        :default-sort="{ prop: 'created_time', order: 'descending' }"
        @selection-change="handleSelectionChange"
        ref="fileTable"
        :selectable="selectableRows"
        max-height="500"
      >
        <el-table-column type="selection" width="60"></el-table-column>
        <el-table-column prop="relative_path" label="文件名" width="800"></el-table-column>
        <el-table-column prop="size" label="大小 (字节)"></el-table-column>
        <el-table-column prop="created_time" label="创建时间"></el-table-column>
        <el-table-column prop="modified_time" label="修改时间"></el-table-column>
        <el-table-column label="操作" width="120">
          <template v-slot="scope">
            <el-button @click="downloadFile(scope.row.relative_path)" type="success">下载</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-button
        v-if="selectedFiles.length === 2"
        type="primary"
        @click="startComparison"
        style="margin-top: 20px;"
      >
        开始比对
      </el-button>
    </el-main>
  </el-container>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';

export default {
  setup() {
    const files = ref([]);
    const selectedFiles = ref([]);
    const fileTable = ref(null); // 用于引用表格

    const fetchFiles = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8099/files');
        files.value = response.data;
      } catch (error) {
        console.error("加载文件失败:", error);
        alert("加载文件失败，请检查控制台");
      }
    };

    const downloadFile = (filename) => {
      const url = `http://127.0.0.1:8099/download?file=${encodeURIComponent(filename)}`;
      window.open(url);
    };

    const handleSelectionChange = (selection) => {
      // 限制选择数量
      if (selection.length > 2) {
        const limitedSelection = selection.slice(0, 2);
        selectedFiles.value = limitedSelection; // 更新选中项
        updateSelection(limitedSelection); // 更新表格状态
      } else {
        selectedFiles.value = selection; // 更新选中项
      }
    };

    const updateSelection = (selection) => {
      if (fileTable.value) {
        fileTable.value.clearSelection(); // 清除当前选择
        selection.forEach(item => {
          fileTable.value.toggleRowSelection(item, true); // 重新选择
        });
      }
    };

    const startComparison = () => {
      alert(`开始比对: ${selectedFiles.value.map(file => file.name).join(', ')}`);
    };

    onMounted(() => {
      fetchFiles();
    });

    return {
      files,
      fetchFiles,
      downloadFile,
      handleSelectionChange,
      selectedFiles,
      startComparison,
      fileTable
    };
  }
};
</script>

<style scoped>
h1 {
  text-align: center;
  margin-bottom: 20px;
}

.el-table {
  width: 100%;
}

.el-table__header {
  width: 100% !important;
}

.el-table__body {
  width: 100% !important;
}
</style>