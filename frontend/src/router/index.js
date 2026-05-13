import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Home from '../views/Home.vue'
import BookStock from '../views/BookStock.vue'
import BookQuery from '../views/BookQuery.vue'
import Borrow from '../views/Borrow.vue'
import Return from '../views/Return.vue'
import CardManage from '../views/CardManage.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  {
    path: '/home',
    component: Home,
    meta: { requiresAuth: true },
    children: [
      { path: 'book-stock', component: BookStock },
      { path: 'book-query', component: BookQuery },
      { path: 'borrow', component: Borrow },
      { path: 'return', component: Return },
      { path: 'card-manage', component: CardManage },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫：未登录跳转到登录页
router.beforeEach((to, from, next) => {
  const admin = localStorage.getItem('admin')
  if (to.meta.requiresAuth && !admin) {
    next('/login')
  } else {
    next()
  }
})

export default router