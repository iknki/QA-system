import request from '@/utils/request'

// 注册接口
export const userRegisterService = ({Username, Password, rePassword}) => {
    return request({
        url: '/api/register',
        method: 'post',
        data: {
            Username: Username,
            Password: Password
        }
    })
}

export const userLoginService = ({Username, Password}) => {
    return request({
        url: '/api/login',
        method: 'post',
        data: {
            'Username': Username,
            'Password': Password
        }
    })
}