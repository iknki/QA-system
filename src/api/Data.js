import request from '@/utils/request'

// 获取知识列表
export const dataGetDataOverviewService = ({userid,}) => {
    console.log(userid)
    return request({
        url: '/api/data/GetDataOverview',
        method: 'get',
        params: {
            userid: userid,
        },
    })
}

export const dataGetViewsService = () => {
    return request({
        url: '/api/data/GetDataViews',
        method: 'get',
    })
}