<script setup>

import PageContainer from "@/components/PageContainer.vue";
import {ref, onMounted, watch} from "vue";
import {useUserStore} from "@/stores/index.js";
import {modelDeleteModelService, modelGetModelListService, modelCreateModelService} from "@/api/model.js";
import {knowledgeGetKnowledgeListService} from "@/api/Knowledge.js";
import ModelEdit from "@/components/ModelEdit.vue";
import ModelSelect from "@/components/ModelSelect.vue";
import KBSelect from "@/components/KBSelect.vue";
import {ElMessage} from "element-plus";


const modelList = ref([]);
const userStore = useUserStore()
const table_loading = ref(false);
const table_loading2 = ref(false);
const dialog = ref();
const isAddModel = ref(false)
const isSelectData = ref(false)
const newModel = ref({
  pastmodelid: null,
  modelname: '',
  info: '',
  TotalSelect: 0 // 选择要训练的数据总数
})
const formRef = ref()

const params = ref({
  pagenum: 1, // 当前页码
  pagesize: 5, // 每页显示条数
  userid: userStore.token.id, // 用户id
  kbid: null, // 知识库id
  title: '', // 知识标题
  istrain: ''
})

const knowledgeList = ref([])
const total = ref(0) // 总数

const checkboxGroup = ref([])

// 获得知识列表
const getKnowledgeList = async() => {
  try {
    table_loading2.value = true;
    // 调用 knowledgeGetKnowledgeListService 获取历史会话信息
    console.log('knowledgeGetKnowledgeListService is running')
    const response = await knowledgeGetKnowledgeListService(params.value);
    // 更新知识列表
    knowledgeList.value = response.knowledgelist;
    // 更新总数
    total.value = response.total;
    console.log('knowledgeList',knowledgeList)
    table_loading2.value = false;

    // 初始化checkboxGroup, 用于选择要训练的数据
    if (checkboxGroup.value.length !== total.value) {
      const checkboxs = Array.from({ length: total.value }, () => ({ checked: false, knowledgeid: null }));
      checkboxGroup.value = checkboxs
      for (let i = (params.value.pagenum-1)*params.value.pagesize; i < params.value.pagenum*params.value.pagesize; i++) {
        checkboxGroup.value[i].knowledgeid = knowledgeList.value[i-(params.value.pagenum-1)*params.value.pagesize].knowledgeid
      }
    }
  } catch (error) {
    // 如果获取历史对话信息失败，则显示错误消息
    ElMessage.error('获取知识列表失败，请重试！');
    console.error('Error fetching KnowledgeList:', error);
    table_loading2.value = false;
  }
}

const isSelectAllData = ref(false)
watch(isSelectAllData, () => {
  checkboxGroup.value.forEach(item => {
    item.checked = isSelectAllData.value
  })
  newModel.value.TotalSelect = isSelectAllData.value ? total.value : 0
})


// 重置搜索条件
const onReset = () => {
  checkboxGroup.value.forEach(item => {
    item.checked = false
    isSelectAllData.value = false
  })
  newModel.value.TotalSelect = 0
}


watch(params, () => {
      getKnowledgeList()
    }, {deep: true}
)


const rules = {
  modelname: [
    {required: true, message: '请输入知识库名称', trigger: 'blur'},
    {
      pattern: /^\S{1,10}$/,
      message: '知识库名称长度不能超过10个字符',
      trigger: 'blur'
    }
  ],
  TotalSelect: [
    {
      validator: (rule, value, callback) => {
        if (value === 0) {
          callback(new Error('请选择要训练的数据'));
        } else {
          callback();
        }
      },
      trigger: 'submit'
    }
  ]
}

const SelectData = () => {
  isSelectData.value = !isSelectData.value
}

const onSelect = (row) => {
  console.log('onSelect')
  const index = knowledgeList.value.findIndex(item => item.knowledgeid === row.knowledgeid)
  if(checkboxGroup.value[index].checked) {
    newModel.value.TotalSelect += 1
  } else {
    newModel.value.TotalSelect -= 1
  }
}



// 删除知识库
const onDeleteModel = async (row) => {
  await ElMessageBox.confirm('此操作将永久删除该模型, 是否继续?', '温馨提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  });
  try {
    console.log('onDeleteModel')
    const response = await modelDeleteModelService({
      modelid: row.modelid,
      userid: userStore.token.id
    });
    ElMessage.success(response.message)
    console.log('Success Delete Model')
    getModelList();
  } catch (error) {
    // 如果获取历史对话信息失败，则显示错误消息
    ElMessage.error('删除知识库失败:', error.message);
    console.error('Error Delete KB:', error);
  }
}
// 编辑知识库
const onEditModel = (row) => {
  console.log('onEditModel')
  dialog.value.openDialog(row)
}
// 添加知识库
const onAddModel = () => {
  console.log('onAddModel')
  isAddModel.value = !isAddModel.value
}

// 成功回调
const onSuccess = () => {
  getModelList()
}

const isSubmitloading = ref(false)
// 提交
const onSubmit = async () => {
  isSubmitloading.value = true
  console.log('onSubmit')
  await formRef.value.validate()
  // 新建模型
  const response = await modelCreateModelService({
    model: newModel.value,
    knowledgeIDList: checkboxGroup.value.filter(item => item.checked).map(item => item.knowledgeid),
    userid: userStore.token.id
  })
  ElMessage.success(response.message)
  isSubmitloading.value = false
  isAddModel.value = false
  getModelList()
}


const getModelList = async () => {
  try {
    table_loading.value = true;
    // 调用 modelGetModelListService 获取历史会话信息
    console.log('modelGetModelListService is running')
    const response = await modelGetModelListService({userid: userStore.token.id});
    modelList.value = response.modellist;
    console.log('modellist', modelList)
    table_loading.value = false;
  } catch (error) {
    // 如果获取历史对话信息失败，则显示错误消息
    ElMessage.error('获取模型列表失败，请重试！');
    console.error('Error fetching ModelList:', error);
    table_loading.value = false;
  }
};

onMounted(() => {
  console.log("mounted");
  getModelList();
  getKnowledgeList()
})


</script>

<template>
  <el-main>
    <PageContainer :title=" isAddModel ? '' : '现有模型'">
      <template #header>
        <h1 style="margin-top: 0">问题推荐模型训练</h1>
      </template>
      <template #extra>
        <el-button type="danger" @click="onAddModel" v-if="isAddModel">
            取消训练
          <template #icon>
            <i-ep-close/>
          </template>
        </el-button>
        <el-button type="primary" @click="onAddModel" v-else>
          训练新模型
          <template #icon>
            <i-ep-plus/>
          </template>
        </el-button>
      </template>
      <el-table :data="modelList" style="width: 100%" v-loading="table_loading" v-if="!isAddModel">
        <el-table-column type="index" label="序号" width="60px" align="center"></el-table-column>
        <el-table-column prop="modelname" label="模型名称" align="center"></el-table-column>
        <el-table-column prop="info" label="模型信息" align="center"></el-table-column>
        <el-table-column prop="status" label="状态" align="center"></el-table-column>
        <el-table-column prop="timestamp" label="创建时间" align="center"></el-table-column>
        <el-table-column prop="username" label="拥有者" align="center"></el-table-column>
        <el-table-column label="操作" width="100px" align="center">
          <template #default="{row, $index}">
            <el-button type="primary" circle plain @click="onEditModel(row)">
              <el-icon>
                <i-ep-edit/>
              </el-icon>
            </el-button>
            <el-button type="danger" circle plain @click="onDeleteModel(row)">
              <el-icon>
                <i-ep-delete/>
              </el-icon>
            </el-button>
          </template>
        </el-table-column>
        <template #empty>
          <el-empty description="暂无数据"></el-empty>
        </template>
      </el-table>
      <el-form
          ref="formRef"
          :rules="rules"
          :model="newModel"
          label-width="auto"
          :label-position="'right'"
          v-else
          v-loading="isSubmitloading"
      >
        <el-form-item label="选择历史模型" style="margin-bottom: 20px; width: 300px" prop="pastmodelid">
          <ModelSelect v-model="newModel.pastmodelid"></ModelSelect>
        </el-form-item>
        <el-form-item label="模型名称" style="margin-bottom: 20px; width: 300px" prop="modelname" >
          <el-input placeholder="请输入新模型名称" v-model="newModel.modelname">
          </el-input>
        </el-form-item>
        <el-form-item label="模型信息" style="margin-bottom: 20px; width: 600px" prop="info">
          <el-input
              placeholder="请输入模型信息"
              v-model="newModel.info"
              :rows="2"
              type="textarea"
              resize="none"
          >
          </el-input>
        </el-form-item>
        <el-form-item v-if="!isSelectData" prop="TotalSelect">
          <el-button type="primary" @click="SelectData">选择要训练的数据</el-button>
          <span style="margin-left: 20px; ">已经选择了{{newModel.TotalSelect}}条数据</span>
        </el-form-item>
        <h4 v-if="isSelectData">请选择要训练的数据</h4>
        <el-form-item v-if="isSelectData">
          <el-form inline>
            <el-form-item style="width: 240px" label="知识库:">
              <KBSelect v-model="params.kbid"></KBSelect>
            </el-form-item>
            <el-form-item style="width: 160px" label="状态:">
              <el-select v-model="params.istrain" style="width: 182px">
                <el-option label="未训练" value="false"></el-option>
                <el-option label="已训练" value="true"></el-option>
                <el-option label="全部" value=""></el-option>
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button @click="onReset" style="margin-left: 20px">重置选择</el-button>
            </el-form-item>
            <el-form-item>
              <el-button type="success" @click="SelectData">选择完毕</el-button>
            </el-form-item>
          </el-form>
          <!-- 表格区域 -->
          <el-table
              :data="knowledgeList"
              style="width: 100%"
              v-loading="table_loading2"
          >
            <el-table-column width="80px">
              <template #header>
                <el-checkbox v-model="isSelectAllData" label="全选"></el-checkbox>
              </template>
              <template #default="{row, $index}">
                <el-checkbox v-model="checkboxGroup[$index + params.pagesize * (params.pagenum - 1)].checked" @change="onSelect(row)"></el-checkbox>
              </template>
            </el-table-column>
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
            <el-table-column
                label="状态"
                prop="istrain"
                align="center"
            >
              <template #default="{row}">
                <span v-if="row.istrain==='true'" :style="{ color: 'blue'}">已训练</span>
                <span v-else :style="{ color: 'gray'}">未训练</span>
              </template>
            </el-table-column>
            <template #empty>
              <el-empty description="暂无数据"></el-empty>
            </template>
          </el-table>
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
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">提交</el-button>
          <el-button @click="onAddModel">取消</el-button>
        </el-form-item>
      </el-form>
      <ModelEdit ref="dialog" @success="onSuccess"></ModelEdit>
    </PageContainer>
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