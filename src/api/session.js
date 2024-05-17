import request from '@/utils/request'

// 获取会话列表SessionList
export const sessionGetSessionListService = ({userId}) => {
    return request({
        url: '/api/session/GetSessionList',
        method: 'get',
        params: {
            userid:userId
        },
    })
}

// 创建Session
export const sessionCreateSessionService = ({userId, sessionname}) => {
    return request({
        url: '/api/session/CreateSession',
        method: 'post',
        data: {
            userId:userId,
            sessionname:sessionname
        },
    })
}

// 删除Session
export const sessionDeleteSessionService = ({sessionId, userId}) => {
    return request({
        url: '/api/session/DeleteSession',
        method: 'post',
        data: {
            sessionId:sessionId,
            userId:userId
        },
    })
}