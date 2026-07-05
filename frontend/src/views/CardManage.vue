<template>
  <div>
    <h2>借书证管理</h2>

    <div class="section">
      <h3>新增借书证</h3>
      <div class="form-grid">
        <label>卡号<input v-model="form.card_no" /></label>
        <label>姓名<input v-model="form.name" /></label>
        <label>单位<input v-model="form.unit" /></label>
        <label>类别
          <select v-model="form.category">
            <option value="学生">学生</option>
            <option value="教师">教师</option>
            <option value="其他">其他</option>
          </select>
        </label>
      </div>
      <button @click="submitAdd">新增</button>
      <p :class="addMsg.ok ? 'success' : 'error'" v-if="addMsg.text">{{ addMsg.text }}</p>
    </div>

    <div class="section">
      <h3>删除借书证</h3>
      <div class="row">
        <input v-model="delCardNo" placeholder="输入卡号" />
        <button class="btn-del" @click="submitDel">删除</button>
      </div>
      <p :class="delMsg.ok ? 'success' : 'error'" v-if="delMsg.text">{{ delMsg.text }}</p>
    </div>

    <!-- 新增：恢复借书证 -->
    <div class="section">
      <h3>恢复借书证</h3>
      <div class="row">
        <input v-model="restoreCardNo" placeholder="输入已失效的卡号" />
        <button class="btn-restore" @click="submitRestore">恢复</button>
      </div>
      <p :class="restoreMsg.ok ? 'success' : 'error'" v-if="restoreMsg.text">{{ restoreMsg.text }}</p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { addCard, deleteCard, restoreCard } from '../api/cards'

const form = reactive({ card_no: '', name: '', unit: '', category: '学生' })
const addMsg = reactive({ ok: false, text: '' })
const delCardNo = ref('')
const delMsg = reactive({ ok: false, text: '' })
const restoreCardNo = ref('')
const restoreMsg = reactive({ ok: false, text: '' })

async function submitAdd() {
  const res = await addCard({ ...form })
  addMsg.ok = res.success
  addMsg.text = res.message
}

async function submitDel() {
  if (!delCardNo.value) return
  const res = await deleteCard(delCardNo.value)
  delMsg.ok = res.success
  delMsg.text = res.message
}

// 新增：恢复借书证
async function submitRestore() {
  if (!restoreCardNo.value) {
    restoreMsg.ok = false
    restoreMsg.text = '请输入卡号'
    return
  }
  const res = await restoreCard(restoreCardNo.value)
  restoreMsg.ok = res.success
  restoreMsg.text = res.message
}
</script>

<style scoped>
h2 { margin-bottom: 20px; }
.section { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
h3 { margin-bottom: 14px; }
.form-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 16px; }
label { display: flex; flex-direction: column; font-size: 13px; gap: 4px; }
input, select { padding: 7px; border: 1px solid #ddd; border-radius: 4px; }
button { padding: 8px 20px; background: #409eff; color: white; border: none; border-radius: 4px; cursor: pointer; }
.btn-del { background: #f56c6c; }
.btn-restore { background: #e6a23c; }
.btn-restore:hover { background: #ebb563; }
.row { display: flex; gap: 10px; margin-bottom: 8px; }
.success { color: green; margin-top: 8px; }
.error { color: red; margin-top: 8px; }
</style>