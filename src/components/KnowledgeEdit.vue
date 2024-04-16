<script setup>
import { ref, defineExpose, defineEmits} from 'vue'
import KBSelect from "@/components/KBSelect.vue";
import {knowledgeCreateKnowledgeService, knowledgeEditKnowledgeService} from "@/api/Knowledge.js";
import {useUserStore} from "@/stores/index.js";
import { QuillEditor} from "@vueup/vue-quill";
import '@vueup/vue-quill/dist/vue-quill.snow.css';

const defaultformModel = ref({
  title: '', // 知识标题
  kbid: null, // 知识库id
  info: '', // 知识内容
  istrain: 'false' // 是否训练
})
const formModel = ref({})
const formRef = ref()

const visibleDrawer = ref(false)
const userStore = useUserStore()
const isloading = ref(false)


const rules = {
  title: [
    {required: true, message: '请输入知识标题', trigger: 'blur'},
    {
      pattern: /^\S{1,50}$/,
      message: '知识标题长度不能超过50个字符',
      trigger: 'blur'
    }
  ],
  kbid: [
    {
      required: true,
      validator: (rule, value, callback) => {
        if (value === null) {
          callback(new Error('请选择要加入的知识库'));
        } else {
          callback();
        }
      },
      trigger: 'submit'
    }
  ],
  info: [
    {required: true, message: '请输入知识内容', trigger: 'blur'}
  ]
}

const emit = defineEmits(['success'])
const onSubmit = async () => {
  isloading.value = true
  const isEdit = formModel.value.knowledgeid
  console.log('onSubmit')
  await formRef.value.validate()
  if(isEdit) {
    // 编辑知识
    console.log('编辑知识')
    const response = await knowledgeEditKnowledgeService({
      Knowledge: formModel.value,
    })
    ElMessage.success(response.message)
    isloading.value = false
  } else {
    // 添加知识
    console.log('添加知识')
    const response = await knowledgeCreateKnowledgeService({
      Knowledge: formModel.value,
      userid: userStore.token.id,
    })
    ElMessage.success(response.message)
    isloading.value = false
  }
  visibleDrawer.value = false
  emit('success')
}


const openDrawer = (row) => {
  console.log('KnowledgeEdit is opening')
  visibleDrawer.value = true // 打开抽屉
  if(row) {
    formModel.value = {...row}
  }
  else {
    formModel.value = {...defaultformModel.value}
  }
  console.log('formModel',formModel)
}


defineExpose({
  openDrawer
})
</script>

<template>
  <el-drawer
      v-model="visibleDrawer"
      direction="rtl"
      size="40%"
      center
      v-loading="isloading"
  >
    <template #title>
      <div style="text-align: center;">{{ formModel.knowledgeid ? '编辑知识': '添加知识' }}</div>
    </template>
    <el-form
        ref="formRef"
        :rules="rules"
        :model="formModel"
        label-width="auto"
        :label-position="'right'"
    >
      <el-form-item label="知识标题" style="width: 80%" prop="title">
        <el-input v-model="formModel.title" placeholder="请输入知识标题"></el-input>
      </el-form-item>
      <el-form-item label="知识库" style="width: 240px" prop="kbid">
        <KBSelect v-model="formModel.kbid"></KBSelect>
      </el-form-item>
      <el-form-item label="状态" style="width: 240px" prop="istrain">
        <el-select v-model="formModel.istrain">
          <el-option label="未训练" value="false"></el-option>
          <el-option label="已训练" value="true"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="知识内容" prop="info">
        <div class="editor">
          <quill-editor
              v-model:content="formModel.info"
              content-type="text"
              theme="snow"
              :options="{placeholder: '请输入知识内容'}"
          ></quill-editor>
        </div>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">提交</el-button>
        <el-button @click="visibleDrawer = false">取消</el-button>
      </el-form-item>
    </el-form>
  </el-drawer>
</template>

<style lang="scss" scoped>

.editor{
  width: 100%;
  :deep(.ql-container) {
    min-height: 300px;
  }
  min-height: 300px;
}


</style>