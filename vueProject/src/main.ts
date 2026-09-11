import { createApp } from 'vue'
import App from './App.vue'

import './assets/main.css'

// 创建并挂载 Vue 应用（不使用路由，保持最小化）
const app = createApp(App)
app.mount('#app')
