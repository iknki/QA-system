import request from '@/utils/request'

// 获取知识库列表
export const knowledgebaseGetKBListService = ({userId}) => {
    return request({
        url: '/api/knowledgebase/GetKBList',
        method: 'get',
        params: {
            userId:userId
        },
    })
}

// 创建知识库
export const knowledgebaseCreateKBService = ({userId, kbname, info}) => {
    return request({
        url: '/api/knowledgebase/CreateKB',
        method: 'post',
        data: {
            userId:userId,
            kbname:kbname,
            info:info
        },
    })
}

// 编辑知识库
export const knowledgebaseEditKBService = ({kbId, kbname, info, userId}) => {
    return request({
        url: '/api/knowledgebase/EditKB',
        method: 'post',
        data: {
            kbId:kbId,
            kbname:kbname,
            info:info,
            userId:userId
        },
    })
}

// 删除知识库
export const knowledgebaseDeleteKBService = ({indices, userId}) => {
    return request({
        url: '/api/knowledgebase/DeleteKB',
        method: 'get',
        params: {
            indices:indices,
            userId:userId
        },
    })
}
