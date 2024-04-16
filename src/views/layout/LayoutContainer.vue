<script setup>
import {ref} from "vue";
import ChatAside from "@/views/chat/ChatAside.vue";
import router from "@/router/index.js";



</script>

<template style="margin: 0;padding: 0">
  <el-container>
    <router-view name="aside"/>
    <el-container>
      <el-header>
        <el-menu :default-active="$route.path" class="el-menu-demo"
                 :ellipsis="false" mode="horizontal" router>
          <h1 style="color: #5274F3">基于深度学习的知识问答和问题推荐系统</h1>
          <div style="flex-grow: 1"/>
          <el-menu-item index="/index" style="float: right">
            <h3 style="font-size: large">首页</h3>
          </el-menu-item>
          <el-menu-item index="/chat" style="float: right">
            <h3 style="font-size: large">知识问答</h3>
          </el-menu-item>
          <el-menu-item index="/backendmanage" style="float: right">
            <h3 style="font-size: large">后台管理</h3>
          </el-menu-item>
          <el-menu-item index="/user" style="float: right">
            <h3 style="font-size: large">个人中心</h3>
          </el-menu-item>
        </el-menu>
      </el-header>
      <router-view/>
    </el-container>
  </el-container>



</template>

<style scoped>
.el-header {
  padding: 0;
  margin: 0;
}
.el-menu-demo {
  //background-color: rgb(231, 248, 255);
  background-color: white;
  border: 0 !important;
  padding-left: 20px;
  padding-right: 80px;
}


.el-container {
  height: 100vh;
  background-color: #f4f6fa
}





</style>