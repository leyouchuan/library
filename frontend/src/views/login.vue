<template>
  <div class="login-container">
    <div class="login-box">
      <h2>图书管理系统登录</h2>

      <div class="form-item">
        <label>管理员ID</label>
        <input v-model="form.admin_id" type="text" placeholder="请输入管理员ID" />
      </div>

      <div class="form-item">
        <label>密码</label>
        <input v-model="form.password" type="password" placeholder="请输入密码" />
      </div>

      <button @click="handleLogin">登录</button>

      <p v-if="message" :class="success ? 'success' : 'error'">{{ message }}</p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { adminLogin } from '../api/admin'
import { useRouter } from 'vue-router'

const router = useRouter()

const form = reactive({
  admin_id: '',
  password: ''
})

const message = ref('')
const success = ref(false)

const handleLogin = async () => {
  try {
    const res = await adminLogin(form)
    if (res.success) {
      success.value = true
      message.value = '登录成功'
      localStorage.setItem('admin', JSON.stringify(res.admin))
      setTimeout(() => {
        router.push('/home/book-query')
      }, 800)
    } else {
      success.value = false
      message.value = res.message || '登录失败'
    }
  } catch (error) {
    success.value = false
    message.value = '请求失败，请检查后端是否启动'
  }
}
</script>

<style scoped>
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
}

.form-item {
  margin-bottom: 16px;
}

.form-item label {
  display: block;
  margin-bottom: 6px;
  font-size: 14px;
}

.form-item input {
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
}

button {
  width: 100%;
  padding: 10px;
  background: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background: #66b1ff;
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
</style>