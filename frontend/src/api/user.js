import request from './request'

// 用户登录
export function userLogin(data) {
  return request.post('/user/login', data)
}

// 获取用户信息
export function getUserInfo(card_no) {
  return request.get(`/user/${card_no}`)
}

// 更新用户信息（支持密码修改）
export function updateUserInfo(card_no, data) {
  return request.put(`/user/${card_no}`, data)
}

// 获取用户借书历史
export function getUserHistory(card_no, include_returned = false) {
  return request.get(`/user/${card_no}/history`, { 
    params: { include_returned } 
  })
}