<script setup>

import router from "@/router/index.js";
import {ref, inject, onMounted} from 'vue'
import {useUserStore} from "@/stores/index.js";
import * as echarts from "echarts";
import {dataGetDataOverviewService, dataGetViewsService} from "@/api/Data.js";

const userStore = useUserStore()

const views = ref([]) // 访问量

const statisticCardData = ref({
  KB: {
    total: 0,
    current: 0,
  },
  Knowledge: {
    total: 0,
    current:0,
  },
  Conversation: {
    total: 0,
    current: 0,
  },
  Model: {
    total: 0,
    current: 0,
  },
  Log: {
    total: 0,
    current: 0,
  },
  User: {
    total: 0,
    current: 0,
  },
})

// 获取数据总览
const getDataOverview = async () => {
  try {
    const response = await dataGetDataOverviewService({userid: userStore.token.id})
    statisticCardData.value = response.dataOverview
    console.log('statisticCardData', statisticCardData.value)
  } catch (error) {
    console.error('Error fetching data overview:', error);
  }
}

// 获取访问量数据
const getViews = async () => {
  try {
    const response = await dataGetViewsService()
    views.value = response.views
    console.log('views', views.value)
  } catch (error) {
    console.error('Error fetching views:', error);
  }
}

// 渲染柱状图
const renderBarChart = () => {
  // 基于准备好的dom，初始化echarts实例
  let Chart = echarts.init(document.getElementById("charts"));
  // 绘制图表
  let options = {
    title: {
      text: "数据统计",
    },
    tooltip: {},
    xAxis: {
      data: ["知识库", "今日问答", "模型","用户"],
    },
    yAxis: {},
    series: [
      {
        name: "销量",
        type: "bar",
        itemStyle: {
          // 可以根据需要设置不同的颜色
          color: function(params) {
            var colorList = ['#c23531', '#61a0a8', '#d48265', '#91c7ae'];
            return colorList[params.dataIndex];
          }
        },
        data: [
          statisticCardData.value.KB.total,
          statisticCardData.value.Conversation.current,
          statisticCardData.value.Model.total,
          statisticCardData.value.User.total
        ],
      },
    ],
  };
  // 渲染图表
  Chart.setOption(options);
}


const generateHourlyTime = ()=> {
  const times = [];
  for (let hour = 0; hour < 24; hour++) {
    times.push(`${hour.toString().padStart(2, '0')}:00`);
  }
  return times;
}

// 渲染折线图
const renderLineChart = () => {
  // 基于准备好的dom，初始化echarts实例
  let Chart = echarts.init(document.getElementById("charts"));
  // 绘制图表
  let options = {
    title: {
      text: "访问量统计",
    },
    tooltip: {},
    xAxis: {
      data: generateHourlyTime(),
    },
    yAxis: {},
    series: [
      {
        name: "访问量",
        type: "line",
        // 这里假设 data 是一天中每个小时的访问量，可以替换为你的数据
        data: views.value,
      },
    ],
  };
  // 渲染图表
  Chart.setOption(options);
}

const init = async () => {
  // 获取数据
  await Promise.all([getViews(), getDataOverview()]);
  // 渲染柱状图
  renderBarChart()
}


onMounted(() => {
  init()
})

</script>

<template>
  <el-main style="height: 100vh">
    <el-row :gutter="16">
      <el-col :span="10">
        <div class="statistic-group">
          <div class="statistic-card-container">
            <el-card shadow="hover" style="margin-right:5px; margin-left: 10px; width: 45%"
                     body-style="padding-bottom:5px">
              <el-statistic :value="statisticCardData.KB.total">
                <template #title>
                  <div style="display: inline-flex; align-items: center">
                    知识库数量
                    <el-tooltip
                        effect="dark"
                        content="已创建的知识库数量"
                        placement="top"
                    >
                      <el-icon style="margin-left: 4px" :size="12">
                        <i-ep-QuestionFilled/>
                      </el-icon>
                    </el-tooltip>
                  </div>
                </template>
              </el-statistic>
              <div class="statistic-footer">
                <div class="footer-item">
                  <div>
                    <span>今日新增</span>
                    <span class="green" style="margin-left: 2px"> {{ statisticCardData.KB.current }} </span>
                    <span class="green"><i-ep-CaretTop/></span>
                  </div>
                  <div style="flex-grow: 1"/>
                  <el-link @click="router.push('/backendmanage/kbmanage/kblist')" style="font-size: 12px; display: flex">
                    新建知识库
                    <i-ep-TopRight/>
                  </el-link>
                </div>
              </div>
            </el-card>
            <el-card shadow="hover" style="margin-right:10px; margin-left: 5px; width: 45%"
                     body-style="padding-bottom:5px">
              <el-statistic :value="statisticCardData.Knowledge.total">
                <template #title>
                  <div style="display: inline-flex; align-items: center">
                    知识数量
                    <el-tooltip
                        effect="dark"
                        content="已添加的知识数量"
                        placement="top"
                    >
                      <el-icon style="margin-left: 4px" :size="12">
                        <i-ep-QuestionFilled/>
                      </el-icon>
                    </el-tooltip>
                  </div>
                </template>
              </el-statistic>
              <div class="statistic-footer">
                <div class="footer-item">
                  <div>
                    <span>今日新增</span>
                    <span class="green" style="margin-left: 2px"> {{ statisticCardData.Knowledge.current }} </span>
                    <span class="green"><i-ep-CaretTop/></span>
                  </div>
                  <div style="flex-grow: 1"/>
                  <el-link @click="router.push('/backendmanage/kbmanage/knowledgelist')" style="font-size: 12px; display: flex">
                    添加知识
                    <i-ep-TopRight/>
                  </el-link>
                </div>
              </div>
            </el-card>
          </div>
          <div class="statistic-card-container">
            <el-card shadow="hover" style="margin-right:5px; margin-left: 10px; width: 45%;"
                     body-style="padding-bottom:5px">
              <el-statistic :value="statisticCardData.Conversation.total">
                <template #title>
                  <div style="display: inline-flex; align-items: center">
                    知识回答数量
                    <el-tooltip
                        effect="dark"
                        content="已进行的知识回答数量"
                        placement="top"
                    >
                      <el-icon style="margin-left: 4px" :size="12">
                        <i-ep-QuestionFilled/>
                      </el-icon>
                    </el-tooltip>
                  </div>
                </template>
              </el-statistic>
              <div class="statistic-footer">
                <div class="footer-item">
                  <div>
                    <span>今日问答</span>
                    <span class="green" style="margin-left: 2px"> {{ statisticCardData.Conversation.current }} </span>
                    <span class="green"><i-ep-CaretTop/></span>
                  </div>
                  <div style="flex-grow: 1"/>
                  <el-link @click="router.push('/chat')" style="font-size: 12px; display: flex">
                    开始体验
                    <i-ep-TopRight/>
                  </el-link>
                </div>
              </div>
            </el-card>
            <el-card shadow="hover"
                     style="margin-right:10px; margin-left: 5px; width: 45%"
                     body-style="padding-bottom:5px"
                     v-if="userStore.token.role === 'admin'"
            >
              <el-statistic :value="statisticCardData.Model.total">
                <template #title>
                  <div style="display: inline-flex; align-items: center">
                    问题推荐模型数量
                    <el-tooltip
                        effect="dark"
                        content="已经训练好的问题推荐模型数量"
                        placement="top"
                    >
                      <el-icon style="margin-left: 4px" :size="12">
                        <i-ep-QuestionFilled/>
                      </el-icon>
                    </el-tooltip>
                  </div>
                </template>
              </el-statistic>
              <div class="statistic-footer">
                <div class="footer-item">
                  <div>
                    <span>正在训练</span>
                    <span class="green" style="margin-left: 2px"> {{ statisticCardData.Model.current }} </span>
                  </div>
                  <div style="flex-grow: 1"/>
                  <el-link @click="router.push('/backendmanage/model/train')" style="font-size: 12px; display: flex">
                    训练新模型
                    <i-ep-TopRight/>
                  </el-link>
                </div>
              </div>
            </el-card>
          </div>
          <div class="statistic-card-container">
            <el-card shadow="hover"
                     style="margin-right:5px; margin-left: 10px; width: 45%;"
                     body-style="padding-bottom:5px"
                      v-if="userStore.token.role === 'admin'"
            >
              <el-statistic :value="statisticCardData.Log.total">
                <template #title>
                  <div style="display: inline-flex; align-items: center">
                    日志数量
                    <el-tooltip
                        effect="dark"
                        content="系统产生的日志数量"
                        placement="top"
                    >
                      <el-icon style="margin-left: 4px" :size="12">
                        <i-ep-QuestionFilled/>
                      </el-icon>
                    </el-tooltip>
                  </div>
                </template>
              </el-statistic>
              <div class="statistic-footer">
                <div class="footer-item">
                  <div>
                    <span>错误日志</span>
                    <span class="red" style="margin-left: 2px"> {{ statisticCardData.Log.current }} </span>
                    <span class="red"><i-ep-WarningFilled/></span>
                  </div>
                  <div style="flex-grow: 1"/>
                  <el-link @click="router.push('/backendmanage/logs')" style="font-size: 12px; display: flex">
                    查看日志
                    <i-ep-TopRight/>
                  </el-link>
                </div>
              </div>
            </el-card>
            <el-card shadow="hover"
                     style="margin-right:10px; margin-left: 5px; width: 45%"
                     body-style="padding-bottom:5px"
                      v-if="userStore.token.role === 'admin'"
            >
              <el-statistic :value="statisticCardData.User.total">
                <template #title>
                  <div style="display: inline-flex; align-items: center">
                    用户数量
                    <el-tooltip
                        effect="dark"
                        content="已注册的用户数量"
                        placement="top"
                    >
                      <el-icon style="margin-left: 4px" :size="12">
                        <i-ep-QuestionFilled/>
                      </el-icon>
                    </el-tooltip>
                  </div>
                </template>
              </el-statistic>
              <div class="statistic-footer">
                <div class="footer-item">
                  <div>
                    <span>今日新增</span>
                    <span class="green" style="margin-left: 2px"> {{ statisticCardData.User.current }} </span>
                    <span class="green"><i-ep-CaretTop/></span>
                  </div>
                  <div style="flex-grow: 1"/>
                </div>
              </div>
            </el-card>
          </div>
          <el-button-group style="margin-left: 10px">
            <el-button @click="renderBarChart" >数据统计图</el-button>
            <el-button @click="renderLineChart" v-if="userStore.token.role === 'admin'">访问量视图</el-button>
          </el-button-group>
          <el-card id="charts"></el-card>
        </div>
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
            <el-card style="width:50%; margin-left: 10px; background: linear-gradient(to right, #2BC0E4,  #EAECC6)"
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
          <div style="display: flex; margin-top: 10px">
            <div style="flex-grow: 1" />
            <el-link @click="router.push('/backendmanage/settings')" style="font-size: 18px; display: flex">
              系统设置
            </el-link>
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

.el-card_body {
  padding-top: 5px;
  padding-bottom: 5px;
}


.statistic-group {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
}


.statistic-footer {
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  font-size: 12px;
  color: var(--el-text-color-regular);
  margin-top: 10px;
}

.statistic-footer .footer-item {
  display: flex;
  align-items: center;
}

.statistic-footer .footer-item span:last-child {
  display: inline-flex;
  align-items: center;
  margin-left: 4px;
}

.green {
  color: var(--el-color-success);
}

.red {
  color: var(--el-color-error);
}
</style>