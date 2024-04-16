<script setup>

import PageContainer from "@/components/PageContainer.vue";
import router from "@/router/index.js";
import { ref, inject, onMounted } from 'vue'
import {useUserStore} from "@/stores/index.js";
import * as echarts from "echarts";

const userStore = useUserStore()

const statisticCardData = [
  {
    title: '知识库数量',
    value: 0,
    icon: 'el-icon-document',
    color: '#409EFF'
  },
  {
    title: '知识数量',
    value: 0,
    icon: 'el-icon-document',
    color: '#67C23A'
  },
  {
    title: '问题数量',
    value: 0,
    icon: 'el-icon-document',
    color: '#F56C6C'
  },
  {
    title: '用户数量',
    value: 0,
    icon: 'el-icon-document',
    color: '#E6A23C'
  }
]

const init = () => {
  // 基于准备好的dom，初始化echarts实例
  let Chart = echarts.init(document.getElementById("charts"));
  // 绘制图表
  let options = {
    title: {
      text: "数据统计",
    },
    tooltip: {},
    xAxis: {
      data: ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"],
    },
    yAxis: {},
    series: [
      {
        name: "销量",
        type: "bar",
        data: [5, 20, 36, 10, 10, 20],
      },
    ],
  };

  // 渲染图表
  Chart.setOption(options);
}


onMounted(() => {
  init()
})

</script>

<template>
  <el-main style="height: 100vh">
    <el-row :gutter="16">
      <el-col :span="10">
        <el-card class="base-container" style="padding: 0; width: 100%">
          <div class="statistic-card-container">
            <el-card shadow="hover" style="margin-right:10px">
              <el-statistic :value="98500">
                <template #title>
                  <div style="display: inline-flex; align-items: center">
                    Daily active users
                    <el-tooltip
                        effect="dark"
                        content="Number of users who logged into the product in one day"
                        placement="top"
                    >
                      <el-icon style="margin-left: 4px" :size="12">
                        <i-ep-Warning/>
                      </el-icon>
                    </el-tooltip>
                  </div>
                </template>
              </el-statistic>
            </el-card>
            <el-card shadow="hover" style="margin-left:10px">
              <el-statistic :value="98500">
                <template #title>
                  <div style="display: inline-flex; align-items: center">
                    Daily active users
                    <el-tooltip
                        effect="dark"
                        content="Number of users who logged into the product in one day"
                        placement="top"
                    >
                      <el-icon style="margin-left: 4px" :size="12">
                        <i-ep-Warning/>
                      </el-icon>
                    </el-tooltip>
                  </div>
                </template>
              </el-statistic>
            </el-card>
          </div>
          <div class="statistic-card-container">
            <el-card shadow="hover" style="margin-right:10px">
              <el-statistic :value="98500">
                <template #title>
                  <div style="display: inline-flex; align-items: center">
                    Daily active users
                    <el-tooltip
                        effect="dark"
                        content="Number of users who logged into the product in one day"
                        placement="top"
                    >
                      <el-icon style="margin-left: 4px" :size="12">
                        <i-ep-Warning/>
                      </el-icon>
                    </el-tooltip>
                  </div>
                </template>
              </el-statistic>
            </el-card>
            <el-card shadow="hover" style="margin-left:10px">
              <el-statistic :value="98500">
                <template #title>
                  <div style="display: inline-flex; align-items: center">
                    Daily active users
                    <el-tooltip
                        effect="dark"
                        content="Number of users who logged into the product in one day"
                        placement="top"
                    >
                      <el-icon style="margin-left: 4px" :size="12">
                        <i-ep-Warning/>
                      </el-icon>
                    </el-tooltip>
                  </div>
                </template>
              </el-statistic>
            </el-card>
          </div>
          <div class="statistic-card-container">
            <el-card shadow="hover" style="margin-right:10px">
              <el-statistic :value="98500">
                <template #title>
                  <div style="display: inline-flex; align-items: center">
                    Daily active users
                    <el-tooltip
                        effect="dark"
                        content="Number of users who logged into the product in one day"
                        placement="top"
                    >
                      <el-icon style="margin-left: 4px" :size="12">
                        <i-ep-Warning/>
                      </el-icon>
                    </el-tooltip>
                  </div>
                </template>
              </el-statistic>
            </el-card>
            <el-card shadow="hover" style="margin-left:10px">
              <el-statistic :value="98500">
                <template #title>
                  <div style="display: inline-flex; align-items: center">
                    Daily active users
                    <el-tooltip
                        effect="dark"
                        content="Number of users who logged into the product in one day"
                        placement="top"
                    >
                      <el-icon style="margin-left: 4px" :size="12">
                        <i-ep-Warning/>
                      </el-icon>
                    </el-tooltip>
                  </div>
                </template>
              </el-statistic>
            </el-card>
          </div>
          <el-card id="charts"></el-card>
        </el-card>
      </el-col>
      <el-col :span="14">
        <el-card class="base-container" style="background-color: white">
          <el-card
              style="
              width: 100%;
              color: #5274F3;
              align-items: center;
              display: flex;
              margin-bottom: 30px;
              border: none"
              shadow="always
              "
          >
            <div style="font-size: 40px">欢迎体验知识问答和问题推荐系统</div>
            <div style="color: gray; font-size: 16px">提供大模型应用与问题推荐的知识问答服务</div>
          </el-card>
          <div style="display: flex; margin-top: 20px; height: 30vh">
            <el-card
                style="width:50%; margin-right: 10px; background: linear-gradient(to right, #1FA2FF, #12D8FA, #A6FFCB)"
                shadow="hover"
            >
              <i-ep-comment style="font-size: 20px; color: white"/>
              <div style="font-size: 36px; margin-top: 20px; margin-bottom: 10px; color: white">
                知识回答
              </div>
              <div style="color: white; margin-bottom: 20px">
                体验知识回答功能，解答你的疑惑
              </div>
              <el-link @click="router.push('/chat')">开始体验
                <i-ep-TopRight/>
              </el-link>
            </el-card>
            <el-card style="width:50%; margin-left: 10px; background: linear-gradient(to right, #EAECC6, #2BC0E4)"
                     shadow="hover"
            >
              <i-ep-platform style="font-size: 20px; color: white"/>
              <div style="font-size: 36px; margin-top: 20px; margin-bottom: 10px; color: white">
                后台管理
              </div>
              <div style="color: white; margin-bottom: 20px">
                管理你的知识库，建立你的知识体系
              </div>
              <el-link @click="router.push('/backendmanage')">开始体验
                <i-ep-TopRight/>
              </el-link>
            </el-card>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </el-main>
</template>

<style lang="scss" scoped>

.el-row {
  height: 100%;
}

.base-container {
  min-height: 100%;
  background-color: transparent;
  border: none;
  box-shadow: none;
  display: flex;
  justify-content: center;
  align-items: center;
}

.statistic-card-container {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

#charts {
  width: 100%;
  height: 300px;
}

</style>