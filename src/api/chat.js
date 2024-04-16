import request from '@/utils/request'

// 获取历史对话接口
export const chatGetMessagesService = ({sessionId}) => {
    return request({
        url: '/api/chat/GetConversationHistory',
        method: 'get',
        params: {
            sessionId:sessionId
        },
        timeout: 60000 //防止回答时间过长导致超时
    })
}

// 获取对话回答接口
export const chatGetAnswerService = ({sessionId,question}) => {
    console.log('sessionId',sessionId,'question',question)
    return request({
        url: '/api/chat/GetChatAnswer',
        method: 'post',
        data: {
            sessionId:sessionId,
            question:question
        },
        timeout: 60000 //防止回答时间过长导致超时
    })
}
