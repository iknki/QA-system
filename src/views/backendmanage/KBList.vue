<script setup>

import PageContainer from "@/components/PageContainer.vue";
import { ref, onMounted } from "vue";
import {knowledgebaseDeleteKBService, knowledgebaseGetKBListService} from "@/api/knowledgebase.js";
import {useUserStore} from "@/stores/index.js";
import KBEdit from "@/components/KBEdit.vue";

const kblist = ref([]);
const userStore = useUserStore()
const table_loading = ref(false);
const dialog = ref();


// 删除知识库
const onDeleteKB = async (row) => {
  await ElMessageBox.confirm('此操作将永久删除该知识库, 是否继续?', '温馨提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  });
  try {
    console.log('onDeleteKB')
    const response = await knowledgebaseDeleteKBService({indices: row.indices});
    ElMessage.success(response.message)
    console.log('Success Delete KB')
    getKBList();
  } catch(error) {
    // 如果获取历史对话信息失败，则显示错误消息
    ElMessage.error('删除知识库失败:', error.message);
    console.error('Error Delete KB:', error);
  }
}
// 编辑知识库
const onEditKB = (row, $index) => {
  console.log('onEditKB')
  dialog.value.openDialog(row, $index)
}
// 添加知识库
const onAddKB = () => {
  console.log('onAddKB')
  dialog.value.openDialog()
}

// 成功回调
const onSuccess = () => {
  getKBList()
}

const getKBList = async () => {
  try {
    table_loading.value = true;
    // 调用 knowledgebaseGetKBListService 获取历史会话信息
    console.log('knowledgebaseGetKBListService is running')
    const response = await knowledgebaseGetKBListService({userId: userStore.token.id});
    kblist.value = response.kblist;
    console.log('kblist',kblist)
    table_loading.value = false;
  } catch (error) {
    // 如果获取历史对话信息失败，则显示错误消息
    ElMessage.error('获取知识库列表失败，请重试！');
    console.error('Error fetching KBList:', error);
    table_loading.value = false;
  }
};

onMounted( () => {
  console.log("mounted");
  getKBList();
})


</script>

<template>
  <el-main>
    <PageContainer title="知识库列表">
      <template #extra>
        <el-button type="primary" @click="onAddKB">
          新建知识库
          <template #icon>
            <i-ep-plus />
          </template>
        </el-button>
      </template>
      <el-table :data="kblist" style="width: 100%" v-loading="table_loading">
        <el-table-column type="index" label="序号" width="60px" align="center"></el-table-column>
        <el-table-column prop="kbname" label="知识库名称" align="center"></el-table-column>
        <el-table-column prop="info" label="知识库信息" align="center"></el-table-column>
        <el-table-column prop="datacount" label="知识数目" align="center"></el-table-column>
        <el-table-column prop="timestamp" label="创建/修改时间" align="center"></el-table-column>
        <el-table-column prop="username" label="拥有者" align="center"></el-table-column>
        <el-table-column label="操作" width="100px" align="center">
          <template #default="{row, $index}">
            <el-button type="primary" circle plain @click="onEditKB(row, $index)">
              <el-icon >
                <i-ep-edit />
              </el-icon>
            </el-button>
            <el-button type="danger"  circle plain @click="onDeleteKB(row, $index)">
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
      <KBEdit ref="dialog" @success="onSuccess"></KBEdit>
    </PageContainer>
  </el-main>
</template>

<style scoped>

</style>