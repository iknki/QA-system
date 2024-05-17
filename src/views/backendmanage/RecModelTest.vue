<script setup>

import PageContainer from "@/components/PageContainer.vue";
import ModelSelect from "@/components/ModelSelect.vue";
import { ref } from 'vue'
import {useUserStore} from "@/stores/index.js";
import {modelTestModelService} from "@/api/model.js";

const success = ref(true)
const userStore = useUserStore()
const formRef = ref()
const loading = ref(false)

const params = ref({
  modelid: null,
  question: ''
})

const questionList = ref([])

const rules = {
  modelid: [
    {
      required: true,
      validator: (rule, value, callback) => {
        if (value === null) {
          callback(new Error('请选择要测试的模型'));
        } else {
          callback();
        }
      },
      trigger: 'submit'
    }
  ],
  question: [
    {required: true, message: '请输入要测试的问题', trigger: 'blur'}
  ]
}

const TestModel = async () => {
  try {
    await formRef.value.validate()
    loading.value = true
    const response = await modelTestModelService({
      params:params.value,
      userid: userStore.token.id
    })
    questionList.value = response.questionList
    console.log('questionList', questionList.value)
    loading.value = false
  } catch (error) {
    console.log('error', error)
    loading.value = false
  }
}

const onReset = () => {
  formRef.value.resetFields()
  questionList.value = []
}


</script>

<template>
  <el-main>
    <page-container title="问题推荐模型训练">
      <el-form
          ref="formRef"
          :rules="rules"
          :model="params"
          label-width="auto"
          :label-position="'right'"
      >
        <el-form-item label="选择要测试的模型" style="margin-bottom: 20px; width: 300px" prop="modelid">
          <ModelSelect v-model="params.modelid"></ModelSelect>
        </el-form-item>
        <el-form-item label="测试问题" style="margin-bottom: 20px; width: 400px" prop="question">
          <el-input
              placeholder="请输入要测试的问题"
              v-model="params.question"
              :rows="3"
              type="textarea"
              resize="none"
          >
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="TestModel" style="margin-left: 100px">测试</el-button>
          <el-button @click="onReset">重置</el-button>
        </el-form-item>
      </el-form>
      <el-card style="width: 480px" shadow="never" v-loading="loading" body-style="min-height: 250px">
        <template #header>
          <div>测试结果</div>
        </template>
        <div v-if="success">
          <div v-for="question in questionList"> {{ question }} </div>
        </div>
      </el-card>
    </page-container>
  </el-main>

</template>

<style scoped>

</style>