<template>
  <div class="login-container">
    <div class="header-actions">
      <router-link to="/books" class="public-btn">图书查询</router-link>
    </div>
    <div class="login-box">
      <h2>用户登录</h2>

      <div class="form-item">
        <label>借书证号</label>
        <input v-model="form.card_no" type="text" placeholder="请输入借书证号" />
      </div>

      <div class="form-item">
        <label>密码</label>
        <input v-model="form.password" type="password" placeholder="请输入密码" @keyup.enter="handleLogin" />
      </div>

      <button class="login-btn" @click="handleLogin" :disabled="loading">
        {{ loading ? '登录中...' : '登 录' }}
      </button>

      <p v-if="message" :class="success ? 'success' : 'error'">{{ message }}</p>
      
      <div class="back-link">
        <router-link to="/login">返回管理员登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { userLogin } from '../api/user'

const router = useRouter()

const form = reactive({
  card_no: '',
  password: ''
})

const message = ref('')
const success = ref(false)
const loading = ref(false)

const handleLogin = async () => {
  if (!form.card_no || !form.password) {
    message.value = '请填写完整信息'
    success.value = false
    return
  }
  
  loading.value = true
  message.value = ''
  
  try {
    const res = await userLogin(form)
    if (res.success) {
      success.value = true
      message.value = '登录成功，正在跳转...'
      localStorage.setItem('user', JSON.stringify(res.user))
      setTimeout(() => {
        router.push('/user-home')
      }, 800)
    } else {
      success.value = false
      message.value = res.message || '登录失败'
    }
  } catch (error) {
    success.value = false
    message.value = '请求失败，请检查后端是否启动'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.header-actions {
  position: absolute;
  top: 20px;
  right: 30px;
}
.public-btn {
  display: inline-block;
  padding: 8px 18px;
  background: #3a75c2;
  color: white;
  border-radius: 4px;
  text-decoration: none;
  font-size: 14px;
  transition: all 0.2s;
  border: none;
  cursor: pointer;
}
.public-btn:hover {
  background: #6194ce;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(58, 137, 194, 0.3);
}
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f5f7fa;
}

.login-box {
  width: 360px;
  padding: 30px;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.login-box h2 {
  text-align: center;
  margin-bottom: 24px;
  color: #333;
}

.form-item {
  margin-bottom: 16px;
}

.form-item label {
  display: block;
  margin-bottom: 6px;
  font-size: 14px;
  color: #333;
}

.form-item input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
  font-size: 14px;
}

.form-item input:focus {
  outline: none;
  border-color: #409eff;
}

.login-btn {
  width: 100%;
  padding: 10px;
  background: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

.login-btn:hover:not(:disabled) {
  background: #66b1ff;
}

.login-btn:disabled {
  background: #a6c9ff;
  cursor: not-allowed;
}

.success {
  color: green;
  margin-top: 12px;
  text-align: center;
}

.error {
  color: red;
  margin-top: 12px;
  text-align: center;
}

.back-link {
  margin-top: 16px;
  text-align: center;
  font-size: 14px;
}

.back-link a {
  color: #409eff;
  text-decoration: none;
}

.back-link a:hover {
  text-decoration: underline;
}
</style>