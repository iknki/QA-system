import request from '@/utils/request'

// 获取知识列表
export const knowledgeGetKnowledgeListService = (params) => {
    return request({
        url: '/api/knowledge/GetKnowledgeList',
        method: 'get',
        params: params,
    })
}

// 添加知识
export const knowledgeCreateKnowledgeService = ({Knowledge, userid}) => {
    console.log(Knowledge)
    return request({
        url: '/api/knowledge/CreateKnowledge',
        method: 'post',
        data: {
            kbid: Knowledge.kbid,
            title: Knowledge.title,
            info: Knowledge.info,
            userid: userid,
            istrain: Knowledge.istrain,
        },
    })
}

// 编辑知识
export const knowledgeEditKnowledgeService = ({Knowledge, userid}) => {
    return request({
        url: '/api/knowledge/EditKnowledge',
        method: 'post',
        data: {
            knowledgeid: Knowledge.knowledgeid,
            title: Knowledge.title,
            info: Knowledge.info,
            istrain: Knowledge.istrain,
            userid: userid,
        },
    })
}

// 删除知识
export const knowledgebaseDeleteKBService = ({knowledgeid, userid}) => {
    return request({
        url: '/api/knowledge/DeleteKnowledge',
        method: 'get',
        params: {
            knowledgeid:knowledgeid,
            userid:userid
        },
    })
}
