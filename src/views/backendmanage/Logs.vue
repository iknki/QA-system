<script setup>

import PageContainer from "@/components/PageContainer.vue";
import {ref, onMounted, watch} from "vue";
import {useUserStore} from "@/stores/index.js";
import {logDeleteLogService, logGetLogsService} from "@/api/Log.js";

const logs = ref([]);
const userStore = useUserStore()
const table_loading = ref(false);
const total = ref(0) // 总数

const params = ref({
  pagenum: 1, // 当前页码
  pagesize: 10, // 每页显示条数
  userid: userStore.token.id, // 用户id
})


// 删除知识库
const onDeleteLog = async (row) => {
  await ElMessageBox.confirm('此操作将永久删除该日志, 是否继续?', '温馨提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  });
  try {
    console.log('onDeleteLog')
    const response = await logDeleteLogService({logid: row.logid, userid: userStore.token.id});
    ElMessage.success(response.message)
    console.log('Success Delete log')
    getLogs()
  } catch(error) {
    // 如果获取历史对话信息失败，则显示错误消息
    ElMessage.error('删除日志失败:', error.message);
    console.error('Error Delete log:', error);
  }
}


const getLogs = async () => {
  try {
    table_loading.value = true;
    // 调用 logGetLogsService 获取历史会话信息
    console.log('logGetLogsService is running')
    const response = await logGetLogsService(params.value);
    logs.value = response.logs;
    total.value = response.total;
    console.log('logs',logs)
    table_loading.value = false;
  } catch (error) {
    // 如果获取历史对话信息失败，则显示错误消息
    ElMessage.error('获取日志失败，请重试！');
    console.error('Error fetching Logs:', error);
    table_loading.value = false;
  }
};

watch(params, () => {
      getLogs()
    }, {deep: true}
)

onMounted( () => {
  console.log("mounted");
  getLogs()
})


</script>

<template>
  <el-main>
    <PageContainer title="日志管理">
      <el-table :data="logs" style="width: 100%" v-loading="table_loading">
        <el-table-column prop="logid" label="日志ID" width="80px" align="center"></el-table-column>
        <el-table-column prop="username" label="知识库名称" align="center"></el-table-column>
        <el-table-column prop="logcontent" label="知识库信息" align="center"></el-table-column>
        <el-table-column label="状态" align="center">
          <template #default="{row}">
            <el-tag v-if="row.status === '成功'" type="success">操作成功</el-tag>
            <el-tag v-else type="danger">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="timestamp" label="时间" align="center"></el-table-column>
        <el-table-column label="操作" width="100px" align="center">
          <template #default="{row, $index}">
            <el-button type="danger"  circle plain @click="onDeleteLog(row, $index)">
              <el-icon >
                <i-ep-delete />
              </el-icon>
            </el-button>
          </template>
        </el-table-column>
        <template #empty>
          <el-empty description="暂无数据"></el-empty>
        </template>
      </el-table>
      <!-- 分页区域 -->
      <el-pagination
          v-model:current-page="params.pagenum"
          v-model:page-size="params.pagesize"
          :page-sizes="[3, 5, 7, 10, 15, 20]"
          :background="true"
          layout="jumper, total, sizes, prev, pager, next"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"

      />
    </PageContainer>
  </el-main>
</template>

<style scoped>

.el-pagination {
  margin-top: 20px;
  justify-content: center;
}

</style>