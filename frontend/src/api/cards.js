import request from './request'

export function addCard(data) {
  return request.post('/cards', data)
}

export function deleteCard(card_no) {
  return request.delete(`/cards/${card_no}`)
}