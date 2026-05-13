import request from './request'

export function borrowBook(data) {
  return request.post('/borrow', data)
}

export function returnBook(data) {
  return request.post('/return', data)
}

export function getBorrowedBooks(card_no) {
  return request.get(`/borrowed/${card_no}`)
}