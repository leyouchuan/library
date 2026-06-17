<template>
  <div>
    <div class="header-bar">
      <h2>图书查询</h2>
      <div class="header-actions">
        <!-- 如果是公开访问模式，显示返回登录按钮 -->
        <router-link v-if="isPublic" to="/login" class="btn-back">返回登录</router-link>
      </div>
    </div>

    <div class="search-form">
      <input v-model="form.category" placeholder="类别" />
      <input v-model="form.title" placeholder="书名" />
      <input v-model="form.publisher" placeholder="出版社" />
      <input v-model="form.author" placeholder="作者" />
      <input v-model="form.year_start" placeholder="年份从" type="number" />
      <input v-model="form.year_end" placeholder="年份到" type="number" />
      <input v-model="form.price_min" placeholder="价格最低" type="number" step="0.01" />
      <input v-model="form.price_max" placeholder="价格最高" type="number" step="0.01" />
      <select v-model="form.order_by">
        <option value="title">按书名排序</option>
        <option value="category">按类别排序</option>
        <option value="year">按年份排序</option>
        <option value="price">按价格排序</option>
        <option value="author">按作者排序</option>
      </select>
      <button @click="search">查询</button>
      <button @click="reset" class="btn-reset">重置</button>
    </div>

    <table v-if="books.length">
      <thead>
        <tr>
          <th>书号</th><th>类别</th><th>书名</th><th>出版社</th>
          <th>年份</th><th>作者</th><th>价格</th><th>总藏书量</th><th>库存</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="b in books" :key="b.book_no">
          <td>{{ b.book_no }}</td><td>{{ b.category }}</td><td>{{ b.title }}</td>
          <td>{{ b.publisher }}</td><td>{{ b.year }}</td><td>{{ b.author }}</td>
          <td>{{ b.price }}</td><td>{{ b.total_count }}</td>
          <td :style="{ color: b.stock === 0 ? 'red' : 'green' }">{{ b.stock }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else-if="searched" class="empty">没有找到符合条件的图书</p>
  </div>
</template>

<script setup>
import { reactive, ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { queryBooks } from '../api/books'

const route = useRoute()

const form = reactive({
  category: '', title: '', publisher: '', author: '',
  year_start: '', year_end: '', price_min: '', price_max: '',
  order_by: 'title'
})
const books = ref([])
const searched = ref(false)

// 判断是否是公开访问模式（路径为 /books）
const isPublic = computed(() => route.path === '/books')

function clean(obj) {
  const result = {}
  for (const k in obj) {
    if (obj[k] !== '' && obj[k] !== null && obj[k] !== undefined) result[k] = obj[k]
  }
  return result
}

async function search() {
  books.value = await queryBooks(clean(form))
  searched.value = true
}

function reset() {
  Object.keys(form).forEach(k => { form[k] = k === 'order_by' ? 'title' : '' })
  books.value = []
  searched.value = false
}
</script>

<style scoped>
.header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-bar h2 {
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.btn-back {
  display: inline-block;
  padding: 8px 18px;
  background: #376bd1;
  color: white;
  border-radius: 4px;
  text-decoration: none;
  font-size: 14px;
  transition: all 0.2s;
}

.btn-back:hover {
  background: #2654c0;
}

.search-form {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}

.search-form input, .search-form select {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 140px;
}

button {
  padding: 8px 18px;
  background: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-reset {
  background: #909399;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

th, td {
  border: 1px solid #eee;
  padding: 10px 12px;
  text-align: left;
  font-size: 14px;
}

th {
  background: #f2f6fc;
}

tr:hover {
  background: #f9fafc;
}

.empty {
  color: #909399;
  margin-top: 20px;
}
</style>