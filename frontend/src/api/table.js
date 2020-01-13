import request from '@/utils/request'

export function getList(params) {
  return request({
    url: '/article/list',
    method: 'get',
    params
  })
}

export function postList(data) {
  return request({
    url: '/article/list',
    method: 'post',
    data
  })
}
