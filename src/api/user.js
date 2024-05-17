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

// 登陆接口
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

// 修改密码
export const userEditPasswordService = ({username, oldpassword, newpassword}) => {
    console.log(username)
    return request({
        url: '/api/user/EditPassword',
        method: 'get',
        params: {
            username: username,
            oldpassword: oldpassword,
            newpassword: newpassword
        }
    })
}

// 获取用户列表
export const userGetUserListService = (params) => {
    return request({
        url: '/api/user/GetUserList',
        method: 'get',
        params: params,
    })
}

// 添加用户
export const userCreateUserService = ({username, password, role}) => {
    return request({
        url: '/api/user/CreateUser',
        method: 'post',
        data: {
            Username: username,
            Password: password,
            Role: role
        }
    })
}

// 修改用户信息
export const userEditUserService = ({userid, username, password, role}) => {
    return request({
        url: '/api/user/EditUser',
        method: 'post',
        data: {
            Username: username,
            Password: password,
            UserID: userid,
            Role: role
        }
    })
}

// 删除用户
export const userDeleteUserService = ({userid}) => {
    return request({
        url: '/api/user/DeleteUser',
        method: 'get',
        params: {
            userid: userid
        }
    })
}

// 获取用户信息
export const userGetUserInfoService = ({userid}) => {
    return request({
        url: '/api/user/GetUserInfo',
        method: 'get',
        params: {
            userid: userid
        }
    })
}


// 修改用户信息
export const userEditUserInfoService = ({userInfo, userid}) => {
    console.log(userInfo)
    return request({
        url: '/api/user/EditUserInfo',
        method: 'post',
        data: {
            username: userInfo.username,
            nickname: userInfo.nickname,
            age: userInfo.age,
            sex: userInfo.sex,
            email: userInfo.email,
            phone: userInfo.phone,
            area: userInfo.area,
            job: userInfo.job,
            userid: userid
        }
    })
}