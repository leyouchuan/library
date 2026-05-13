import request from './request'

// 单本入库
export function addBook(data) {
  return request.post('/books', data)
}

// 批量入库（上传文件）
export function batchAddBooks(file) {
  const form = new FormData()
  form.append('file', file)
  return request.post('/books/batch', form, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

// 查询图书
export function queryBooks(params) {
  return request.get('/books', { params })
}