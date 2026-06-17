<template>
  <div class="layout">
    <aside class="sidebar">
      <div class="logo">📚 图书管理系统</div>
      <div class="user-info-sidebar">{{ user.name }} 用户</div>
      <nav>
        <router-link to="/user-home" @click="activeTab = 'info'">个人信息</router-link>
        <router-link to="/user-home/history" @click="activeTab = 'history'">借书历史</router-link>
      </nav>
      <button class="logout" @click="logout">退出登录</button>
    </aside>
    <main class="content">
      <!-- 个人信息 -->
      <div v-if="activeTab === 'info'" class="section">
        <h2>个人信息</h2>
        <div class="info-grid">
          <div class="info-item"><label>借书证号：</label><span>{{ user.card_no }}</span></div>
          <div class="info-item"><label>姓名：</label><span>{{ user.name }}</span></div>
          <div class="info-item"><label>单位：</label><span>{{ user.unit || '未设置' }}</span></div>
          <div class="info-item"><label>类别：</label><span>{{ user.category }}</span></div>
          <div class="info-item"><label>状态：</label><span :style="{ color: user.is_active ? '#67c23a' : '#f56c6c' }">
            {{ user.is_active ? '有效' : '已失效' }}
          </span></div>
        </div>
        <button @click="showEdit = !showEdit">修改信息</button>
      </div>

      <!-- 修改信息 -->
      <div v-if="showEdit" class="section edit-section">
        <h3>修改个人信息</h3>
        <div class="form-grid">
          <div class="form-group">
            <label>姓名</label>
            <input v-model="editForm.name" placeholder="请输入姓名" />
          </div>
          <div class="form-group">
            <label>单位</label>
            <input v-model="editForm.unit" placeholder="请输入单位" />
          </div>
          <div class="form-group">
            <label>类别</label>
            <select v-model="editForm.category">
              <option value="学生">学生</option>
              <option value="教师">教师</option>
              <option value="其他">其他</option>
            </select>
          </div>
        </div>
        <div class="form-actions">
          <button @click="updateInfo" class="btn-save">保存修改</button>
          <button @click="showEdit = false" class="btn-cancel">取消</button>
        </div>
        <p :class="updateMsg.ok ? 'success' : 'error'" v-if="updateMsg.text">{{ updateMsg.text }}</p>
      </div>

      <!-- 借书历史 -->
      <div v-if="activeTab === 'history'" class="section">
        <h2>我的借书历史</h2>
        <div class="history-controls">
          <label>
            <input type="checkbox" v-model="showReturned" @change="loadHistory" />
            显示已归还
          </label>
          <button @click="loadHistory" class="btn-refresh">刷新</button>
        </div>
        
        <div v-if="history.length">
          <table>
            <thead>
              <tr>
                <th>书号</th>
                <th>类别</th>
                <th>书名</th>
                <th>出版社</th>
                <th>年份</th>
                <th>作者</th>
                <th>价格</th>
                <th>借书时间</th>
                <th>归还时间</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="record in history" :key="record.id">
                <td>{{ record.book_no }}</td>
                <td>{{ record.category }}</td>
                <td>{{ record.title }}</td>
                <td>{{ record.publisher }}</td>
                <td>{{ record.year }}</td>
                <td>{{ record.author }}</td>
                <td>￥{{ record.price }}</td>
                <td>{{ record.borrow_time }}</td>
                <td>{{ record.return_time || '未归还' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-else class="empty">暂无借书记录</p>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getUserInfo, updateUserInfo, getUserHistory } from '../api/user'

const router = useRouter()
const activeTab = ref('info')

const user = reactive({
  card_no: '',
  name: '',
  unit: '',
  category: '',
  is_active: true
})

const showEdit = ref(false)
const editForm = reactive({ name: '', unit: '', category: '' })
const updateMsg = reactive({ ok: false, text: '' })
const history = ref([])
const showReturned = ref(false)

async function loadUserInfo() {
  const userData = JSON.parse(localStorage.getItem('user') || '{}')
  if (!userData.card_no) {
    router.push('/user-login')
    return
  }
  
  try {
    const res = await getUserInfo(userData.card_no)
    if (res.success) {
      Object.assign(user, res.user)
      editForm.name = user.name
      editForm.unit = user.unit || ''
      editForm.category = user.category
    } else {
      console.error('获取用户信息失败:', res.message)
    }
  } catch (error) {
    console.error('请求用户信息失败:', error)
    // 如果请求失败，使用 localStorage 中的数据
    if (userData.name) {
      Object.assign(user, userData)
    }
  }
}

async function loadHistory() {
  const userData = JSON.parse(localStorage.getItem('user') || '{}')
  if (!userData.card_no) return
  
  try {
    const res = await getUserHistory(userData.card_no, showReturned.value)
    history.value = res || []
  } catch (error) {
    console.error('加载借书历史失败:', error)
    history.value = []
  }
}

async function updateInfo() {
  if (!editForm.name) {
    updateMsg.ok = false
    updateMsg.text = '姓名不能为空'
    return
  }
  
  try {
    const res = await updateUserInfo(user.card_no, editForm)
    updateMsg.ok = res.success
    updateMsg.text = res.message
    if (res.success) {
      user.name = editForm.name
      user.unit = editForm.unit
      user.category = editForm.category
      // 更新 localStorage
      const userData = JSON.parse(localStorage.getItem('user') || '{}')
      userData.name = editForm.name
      userData.unit = editForm.unit
      userData.category = editForm.category
      localStorage.setItem('user', JSON.stringify(userData))
      setTimeout(() => { 
        showEdit.value = false 
        updateMsg.text = ''
      }, 1500)
    }
  } catch (error) {
    updateMsg.ok = false
    updateMsg.text = '更新失败，请重试'
  }
}

function logout() {
  localStorage.removeItem('user')
  router.push('/user-login')
}

onMounted(() => {
  loadUserInfo()
  loadHistory()
})
</script>

<style scoped>
/* 复用 Home.vue 的布局样式 */
.layout {
  display: flex;
  height: 100vh;
  font-family: 'Microsoft YaHei', sans-serif;
}

.sidebar {
  width: 200px;
  background: #2c3e50;
  color: white;
  display: flex;
  flex-direction: column;
  padding: 20px 0;
  flex-shrink: 0;
}

.logo {
  font-size: 18px;
  font-weight: bold;
  padding: 0 20px 16px;
  border-bottom: 1px solid #3d5166;
}

.user-info-sidebar {
  font-size: 14px;
  color: #aab8c7;
  padding: 12px 20px;
  border-bottom: 1px solid #3d5166;
  margin-bottom: 8px;
}

nav {
  display: flex;
  flex-direction: column;
  flex: 1;
}

nav a {
  color: #cdd8e3;
  text-decoration: none;
  padding: 12px 20px;
  font-size: 14px;
  transition: background 0.2s;
  cursor: pointer;
}

nav a:hover {
  background: #409eff;
  color: white;
}

.logout {
  margin: 12px 20px;
  padding: 8px;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s;
}

.logout:hover {
  background: #c0392b;
}

.content {
  flex: 1;
  padding: 30px;
  background: #f5f7fa;
  overflow-y: auto;
}

/* 内容区域样式 */
.section {
  background: white;
  padding: 24px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
}

h2 {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 20px;
  color: #333;
}

h3 {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 16px;
  color: #555;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}

.info-item {
  padding: 10px 14px;
  background: #f8f9fa;
  border-radius: 4px;
}

.info-item label {
  font-weight: 600;
  margin-right: 8px;
  color: #555;
}

.info-item span {
  color: #333;
}

button {
  padding: 8px 20px;
  background: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s;
  font-size: 14px;
}

button:hover {
  background: #66b1ff;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-weight: 500;
  font-size: 13px;
  color: #555;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  box-sizing: border-box;
  font-size: 14px;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #409eff;
}

.form-actions {
  display: flex;
  gap: 10px;
}

.btn-save {
  background: #67c23a;
}

.btn-save:hover {
  background: #85ce61;
}

.btn-cancel {
  background: #909399;
}

.btn-cancel:hover {
  background: #a8abb2;
}

.btn-refresh {
  background: #86e63c;
}

.btn-refresh:hover {
  background: #c7eb63;
}

.history-controls {
  display: flex;
  gap: 20px;
  align-items: center;
  margin-bottom: 16px;
}

.history-controls label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #555;
  cursor: pointer;
}

.history-controls input[type="checkbox"] {
  width: 16px;
  height: 16px;
  cursor: pointer;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

th, td {
  border: 1px solid #ebeef5;
  padding: 10px 12px;
  text-align: left;
}

th {
  background: #f5f7fa;
  font-weight: 600;
  color: #555;
}

tr:hover {
  background: #fafafa;
}

.success {
  color: #67c23a;
  margin-top: 12px;
  font-size: 14px;
}

.error {
  color: #f56c6c;
  margin-top: 12px;
  font-size: 14px;
}

.empty {
  color: #909399;
  text-align: center;
  padding: 20px 0;
}

/* 响应式 */
@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .sidebar {
    width: 160px;
  }
}
</style>