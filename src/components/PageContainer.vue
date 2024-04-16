<script setup>
import { defineProps } from 'vue'
defineProps({
  title:{
    required: true,
    type: String,
  }
})
</script>

<template>
  <el-card class="page-container">
    <template #header>
      <slot name="header"></slot>
      <div class="header">
        <span>{{title}}</span>
        <div class="extra">
          <slot name="extra"></slot>
        </div>
      </div>
    </template>
    <slot></slot>
  </el-card>
</template>

<style lang="scss" scoped>
.page-container {
  min-height: 100%;
  box-sizing: border-box;
  .header{
    display: flex;
    justify-content: space-between;
    align-items: center;
    .extra {
      display: flex;
      align-items: center;
    }
  }
}

</style>