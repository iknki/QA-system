<script setup>

import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import {provide} from "vue";;

</script>
<template>
<div>
  <el-config-provider :locale="zhCn">
    <router-view></router-view>
  </el-config-provider>


</div>
</template>

<style>

</style>