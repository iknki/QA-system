import request from '@/utils/request'

// 获取知识列表
export const settingGetSettingsService = () => {
    return request({
        url: '/api/setting/GetSettings',
        method: 'get',
    })
}

export const settingEditSettingsService = ({settings}) => {
    return request({
        url: '/api/setting/EditSettings',
        method: 'post',
        data: {
            data:settings,
        },
    })
}