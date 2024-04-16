import request from '@/utils/request'
import { ref } from 'vue'

// 获取知识列表
export const modelGetModelListService = ({userid}) => {
    return request({
        url: '/api/model/GetModelList',
        method: 'get',
        params: {
            userid: userid,
        }
    })
}

// 添加知识
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

// 编辑知识
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

// 删除知识
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
