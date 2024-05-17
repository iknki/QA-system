import request from '@/utils/request'
import { ref } from 'vue'

// 获取模型列表
export const modelGetModelListService = ({userid}) => {
    return request({
        url: '/api/model/GetModelList',
        method: 'get',
        params: {
            userid: userid,
        }
    })
}

// 添加模型
export const modelCreateModelService = ({model, knowledgeIDList, userid}) => {
    return request({
        url: '/api/model/CreateModel',
        method: 'post',
        data: {
            pastmodelid: model.pastmodelid,
            modelname: model.modelname,
            info: model.info,
            userid: userid,
            knowledgeIDList: knowledgeIDList,
        },
    })
}

// 编辑模型
export const modelEditModelService = ({model, userid}) => {
    return request({
        url: '/api/model/EditModel',
        method: 'post',
        data: {
            modelid: model.modelid,
            modelname: model.modelname,
            info: model.info,
            status: model.status,
            userid: userid,
        },
    })
}

// 删除模型
export const modelDeleteModelService = ({modelid, userid}) => {
    return request({
        url: '/api/model/DeleteModel',
        method: 'get',
        params: {
            modelid:modelid,
            userid: userid,
        },
    })
}

// 删除模型
export const modelTestModelService = ({params, userid}) => {
    return request({
        url: '/api/model/TestModel',
        method: 'get',
        params: {
            modelid:params.modelid,
            question:params.question,
            userid: userid,
        },
        timeout: 60000 //防止回答时间过长导致超时
    })
}
