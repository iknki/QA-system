<script setup>
import {onMounted, watch, ref} from 'vue';
import PageContainer from "@/components/PageContainer.vue";
import KBSelect from "@/components/KBSelect.vue";
import {useUserStore} from "@/stores/index.js";
import {knowledgeGetKnowledgeListService, knowledgebaseDeleteKBService} from "@/api/Knowledge.js";
import KnowledgeEdit from "@/components/KnowledgeEdit.vue";

const table_loading = ref(false);
const userStore = useUserStore()
const knowledgeList = ref([])
const total = ref(0) // 总数
const knowledgeEditRef = ref() // 抽屉组件引用

// 定义查询参数
const params = ref({
  pagenum: 1, // 当前页码
  pagesize: 5, // 每页显示条数
  userid: userStore.token.id, // 用户id
  kbid: null, // 知识库id
  title: '', // 知识标题
  istrain: '',
})

// 获得知识列表
const getKnowledgeList = async() => {
  try {
    table_loading.value = true;
    // 调用 knowledgeGetKnowledgeListService 获取历史会话信息
    console.log('knowledgeGetKnowledgeListService is running')
    const response = await knowledgeGetKnowledgeListService(params.value);
    // 更新知识列表
    knowledgeList.value = response.knowledgelist;
    // 更新总数
    total.value = response.total;
    console.log('knowledgeList',knowledgeList)
    table_loading.value = false;
  } catch (error) {
    // 如果获取历史对话信息失败，则显示错误消息
    ElMessage.error('获取知识列表失败，请重试！');
    console.error('Error fetching KnowledgeList:', error);
    table_loading.value = false;
  }
}

// 重置搜索条件
const onReset = () => {
  params.value.kbid = null;
  params.value.title = '';
}


// 添加知识
const onAddKnowledge = () => {
  console.log('onEditKnowledge')
  knowledgeEditRef.value.openDrawer()
}

// 编辑知识
const onEditKnowledge = (row) => {
  console.log('onEditKnowledge')
  knowledgeEditRef.value.openDrawer(row)
}

// 删除逻辑
const onDeleteKnowledge = async (row) => {
  console.log('onDeleteKnowledge')
  await ElMessageBox.confirm('此操作将永久删除该知识, 是否继续?', '温馨提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  });
  try {
    console.log('onDeleteKB')
    const response = await knowledgebaseDeleteKBService({knowledgeid: row.knowledgeid});
    ElMessage.success(response.message)
    console.log('Success Delete Knowledge')
    getKnowledgeList();
  } catch(error) {
    // 如果获取历史对话信息失败，则显示错误消息
    ElMessage.error('删除知识失败:', error.message);
    console.error('Error Delete KB:', error);
  }
}

onMounted( () => {
  getKnowledgeList()
})

watch(params, () => {
  getKnowledgeList()
}, {deep: true}
)

// 成功回调
const onSuccess = () => {
  getKnowledgeList()
}

</script>

<template>
  <el-main>
    <page-container title="知识管理">
      <template #extra>
        <el-button type="primary" @click="onAddKnowledge">
          添加知识
          <template #icon>
            <i-ep-plus />
          </template>
        </el-button>
      </template>
      <!-- 表单区域 -->
      <el-form inline>
        <el-form-item style="width: 240px" label="知识库:">
          <KBSelect v-model="params.kbid"></KBSelect>
        </el-form-item>
        <el-form-item label="知识标题:">
          <el-input  placeholder="请输入知识标题" v-model="params.title"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button @click="onReset">重置</el-button>
        </el-form-item>
      </el-form>
      <!-- 表格区域 -->
      <el-table :data="knowledgeList" style="width: 100%" v-loading="table_loading">
        <el-table-column type="index" label="序号" width="60px" align="center">
          <template #default="{ $index }">
            {{ $index + params.pagesize * (params.pagenum - 1) + 1 }}
          </template>
        </el-table-column>
        <el-table-column label="知识标题" prop="title" align="center"></el-table-column>
        <el-table-column label="知识内容" prop="info" align="center">
          <template #default="{row}">
            <span class="limited-text"> {{ row.info }} </span>
          </template>
        </el-table-column>
        <el-table-column label="知识库" prop="kbname" align="center"></el-table-column>
        <el-table-column label="创建/修改时间" prop="timestamp" align="center"></el-table-column>
        <el-table-column label="状态" prop="istrain" align="center">
          <template #default="{row}">
            <span v-if="row.istrain==='true'" :style="{ color: 'blue'}">已训练</span>
            <span v-else :style="{ color: 'gray'}">未训练</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100px" align="center">
          <template #default="{row, $index}">
            <el-button type="primary" circle plain @click="onEditKnowledge(row)">
              <el-icon >
                <i-ep-edit />
              </el-icon>
            </el-button>
            <el-button type="danger"  circle plain @click="onDeleteKnowledge(row)">
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
      <!-- 抽屉区域 -->
      <KnowledgeEdit ref="knowledgeEditRef" @success="onSuccess">
      </KnowledgeEdit>
    </page-container>
  </el-main>
</template>

<style scoped>
.limited-text {
  max-height: 8em; /* 设置最大高度 */
  overflow: hidden; /* 隐藏溢出内容 */
  display: -webkit-box; /* 使用 flexbox 布局模型 */
  -webkit-line-clamp: 8; /* 设置最大行数 */
  -webkit-box-orient: vertical; /* 垂直方向布局 */
}

.el-pagination {
  margin-top: 20px;
  justify-content: center;
}

</style>