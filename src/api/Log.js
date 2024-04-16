import request from '@/utils/request'

// 获取日志列表
export const logGetLogsService = (params) => {
    console.log(params)
    return request({
        url: '/api/log/GetLogList',
        method: 'get',
        params: params,
    })
}

// 删除日志
export const logDeleteLogService = ({logid, userid}) => {
    return request({
        url: '/api/log/DeleteLog',
        method: 'get',
        params: {
            logid:logid,
            userid:userid,
        },
    })
}
