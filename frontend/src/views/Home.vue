<template>
  <div class="layout">
    <aside class="sidebar">
      <div class="logo">📚 图书管理系统</div>
      <div class="admin-info">{{ admin.name }} 管理员</div>
      <nav>
        <router-link to="/home/book-query">图书查询</router-link>
        <router-link to="/home/book-stock">图书入库</router-link>
        <router-link to="/home/borrow">借书</router-link>
        <router-link to="/home/return">还书</router-link>
        <router-link to="/home/card-manage">借书证管理</router-link>
      </nav>
      <button class="logout" @click="logout">退出登录</button>
    </aside>
    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const admin = reactive(JSON.parse(localStorage.getItem('admin') || '{}'))

function logout() {
  localStorage.removeItem('admin')
  router.push('/login')
}
</script>

<style scoped>
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
}
.logo {
  font-size: 16px;
  font-weight: bold;
  padding: 0 20px 16px;
  border-bottom: 1px solid #3d5166;
}
.admin-info {
  font-size: 13px;
  color: #aab8c7;
  padding: 12px 20px;
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
}
nav a:hover, nav a.router-link-active {
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
}
.content {
  flex: 1;
  padding: 30px;
  background: #f5f7fa;
  overflow-y: auto;
}
</style>