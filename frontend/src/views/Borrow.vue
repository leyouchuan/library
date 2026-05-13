<template>
  <div>
    <h2>借书</h2>
    <div class="section">
      <h3>第一步：输入借书证卡号</h3>
      <div class="row">
        <input v-model="card_no" placeholder="借书证卡号" />
        <button @click="loadBorrowed">查询已借书籍</button>
      </div>

      <div v-if="borrowedBooks.length">
        <p>该借书证当前已借书籍：</p>
        <table>
          <thead><tr><th>书号</th><th>借出时间</th></tr></thead>
          <tbody>
            <tr v-for="r in borrowedBooks" :key="r.id">
              <td>{{ r.book_no }}</td><td>{{ r.borrow_time }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <p v-else-if="queried" class="empty">该借书证暂无已借书籍</p>
    </div>

    <div class="section">
      <h3>第二步：输入要借的书号</h3>
      <div class="row">
        <input v-model="book_no" placeholder="书号" />
        <button @click="doBorrow">确认借书</button>
      </div>
      <p :class="msg.ok ? 'success' : 'error'" v-if="msg.text">{{ msg.text }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { getBorrowedBooks, borrowBook } from '../api/borrow'

const card_no = ref('')
const book_no = ref('')
const borrowedBooks = ref([])
const queried = ref(false)
const msg = reactive({ ok: false, text: '' })

const admin = JSON.parse(localStorage.getItem('admin') || '{}')

async function loadBorrowed() {
  if (!card_no.value) return
  borrowedBooks.value = await getBorrowedBooks(card_no.value)
  queried.value = true
}

async function doBorrow() {
  if (!card_no.value || !book_no.value) {
    msg.ok = false; msg.text = '请填写借书证卡号和书号'; return
  }
  const res = await borrowBook({ card_no: card_no.value, book_no: book_no.value, admin_id: admin.admin_id })
  msg.ok = res.success
  msg.text = res.message
  if (res.success) loadBorrowed()
}
</script>

<style scoped>
h2 { margin-bottom: 20px; }
.section { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
h3 { margin-bottom: 14px; }
.row { display: flex; gap: 10px; margin-bottom: 14px; }
input { padding: 8px; border: 1px solid #ddd; border-radius: 4px; width: 200px; }
button { padding: 8px 18px; background: #409eff; color: white; border: none; border-radius: 4px; cursor: pointer; }
table { width: 100%; border-collapse: collapse; }
th, td { border: 1px solid #eee; padding: 8px 12px; font-size: 14px; }
th { background: #f2f6fc; }
.success { color: green; } .error { color: red; } .empty { color: #909399; }
</style>