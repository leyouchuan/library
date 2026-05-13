<template>
  <div>
    <h2>图书入库</h2>

    <div class="section">
      <h3>单本入库</h3>
      <div class="form-grid">
        <label>书号<input v-model="form.book_no" /></label>
        <label>类别<input v-model="form.category" /></label>
        <label>书名<input v-model="form.title" /></label>
        <label>出版社<input v-model="form.publisher" /></label>
        <label>年份<input v-model="form.year" type="number" /></label>
        <label>作者<input v-model="form.author" /></label>
        <label>价格<input v-model="form.price" type="number" step="0.01" /></label>
        <label>数量<input v-model="form.quantity" type="number" /></label>
      </div>
      <button @click="submitSingle">确认入库</button>
      <p :class="singleMsg.ok ? 'success' : 'error'" v-if="singleMsg.text">{{ singleMsg.text }}</p>
    </div>

    <div class="section">
      <h3>批量入库（上传文件）</h3>
      <p class="hint">文件格式每行：书号, 类别, 书名, 出版社, 年份, 作者, 价格, 数量</p>
      <input type="file" accept=".txt,.csv" @change="onFileChange" />
      <button @click="submitBatch" :disabled="!batchFile">上传入库</button>
      <div v-if="batchResult" class="batch-result">
        <p class="success">成功：{{ batchResult.results.length }} 条</p>
        <p class="error" v-for="e in batchResult.errors" :key="e">{{ e }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { addBook, batchAddBooks } from '../api/books'

const form = reactive({ book_no: '', category: '', title: '', publisher: '', year: '', author: '', price: '', quantity: '' })
const singleMsg = reactive({ ok: false, text: '' })
const batchFile = ref(null)
const batchResult = ref(null)

async function submitSingle() {
  const res = await addBook({
    ...form,
    year: form.year ? parseInt(form.year) : null,
    price: parseFloat(form.price),
    quantity: parseInt(form.quantity)
  })
  singleMsg.ok = res.success
  singleMsg.text = res.message
}

function onFileChange(e) {
  batchFile.value = e.target.files[0]
}

async function submitBatch() {
  if (!batchFile.value) return
  batchResult.value = await batchAddBooks(batchFile.value)
}
</script>

<style scoped>
h2 { margin-bottom: 20px; }
.section { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
h3 { margin-bottom: 16px; }
.form-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 16px; }
label { display: flex; flex-direction: column; font-size: 13px; gap: 4px; }
input { padding: 7px; border: 1px solid #ddd; border-radius: 4px; }
button { padding: 8px 20px; background: #409eff; color: white; border: none; border-radius: 4px; cursor: pointer; }
button:disabled { background: #c0c4cc; }
.hint { color: #909399; font-size: 13px; margin-bottom: 10px; }
.success { color: green; margin-top: 8px; }
.error { color: red; margin-top: 4px; }
</style>