<script setup>

import PageContainer from "@/components/PageContainer.vue";
import ModelSelect from "@/components/ModelSelect.vue";
import { ref } from 'vue'
import {useUserStore} from "@/stores/index.js";

const success = ref(true)
const userStore = useUserStore()
const formRef = ref()


const params = ref({
  modelid: null,
  title: ''
})

const questionList = ref([
  '问题1',
  '问题2',
  '问题3',
  '问题4',
  '问题5',
  '问题6',
  '问题7',
  '问题8',
  '问题9',
  '问题10',

])

</script>

<template>
  <el-main>
    <page-container title="问题推荐模型训练">
      <el-form
          ref="formRef"
          :model="params"
          label-width="auto"
          :label-position="'right'"
      >
        <el-form-item label="选择要测试的模型" style="margin-bottom: 20px; width: 300px" prop="modelid">
          <ModelSelect v-model="params.modelid"></ModelSelect>
        </el-form-item>
        <el-form-item label="测试问题" style="margin-bottom: 20px; width: 400px" prop="title">
          <el-input
              placeholder="请输入要测试的问题"
              v-model="params.title"
              :rows="3"
              type="textarea"
              resize="none"
          >
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit" style="margin-left: 100px">测试</el-button>
          <el-button @click="onSubmit">重置</el-button>
        </el-form-item>
      </el-form>
      <el-card style="width: 480px" shadow="never">
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