import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Home from '../views/Home.vue'
import BookStock from '../views/BookStock.vue'
import BookQuery from '../views/BookQuery.vue'
import Borrow from '../views/Borrow.vue'
import Return from '../views/Return.vue'
import CardManage from '../views/CardManage.vue'
import UserLogin from '../views/UserLogin.vue'
import UserHome from '../views/UserHome.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/user-login', component: UserLogin },
  // 图书查询 - 公开访问，不需要登录
  { 
    path: '/books', 
    component: BookQuery,
    meta: { public: true }
  },
  {
    path: '/home',
    component: Home,
    meta: { requiresAuth: true, role: 'admin' },
    children: [
      { path: 'book-stock', component: BookStock },
      { path: 'book-query', component: BookQuery },
      { path: 'borrow', component: Borrow },
      { path: 'return', component: Return },
      { path: 'card-manage', component: CardManage },
    ]
  },
  {
    path: '/user-home',
    component: UserHome,
    meta: { requiresAuth: true, role: 'user' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  // 公开页面直接放行
  if (to.meta.public) {
    next()
    return
  }
  
  const admin = localStorage.getItem('admin')
  const user = localStorage.getItem('user')
  
  if (to.meta.requiresAuth) {
    if (to.meta.role === 'admin' && admin) {
      next()
    } else if (to.meta.role === 'user' && user) {
      next()
    } else {
      next('/login')
    }
  } else {
    if (admin) {
      next('/home')
    } else if (user) {
      next('/user-home')
    } else {
      next()
    }
  }
})

export default router