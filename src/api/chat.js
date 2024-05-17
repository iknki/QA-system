import request from '@/utils/request'

// 获取历史对话接口
export const chatGetMessagesService = ({sessionId, userId}) => {
    return request({
        url: '/api/chat/GetConversationHistory',
        method: 'get',
        params: {
            sessionId:sessionId,
            userId:userId
        },
        timeout: 60000 //防止回答时间过长导致超时
    })
}

// 获取对话回答接口
export const chatGetAnswerService = ({sessionId, question, userId}) => {
    console.log('sessionId',sessionId,'question',question)
    return request({
        url: '/api/chat/GetChatAnswer',
        method: 'post',
        data: {
            sessionId:sessionId,
            question:question,
            userId: userId
        },
        timeout: 60000 //防止回答时间过长导致超时
    })
}

export const chatGetRecommendQuestionsService = ({question=null, userId, flag=false}) => {
    return request({
        url: '/api/chat/GetRecommendQuestions',
        method: 'get',
        params: {
            question:question,
            userId: userId,
            flag: flag
        },
        timeout: 60000 //防止回答时间过长导致超时
    })
}