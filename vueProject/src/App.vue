<template>
  <div class="app-shell">
    <div class="phone-frame">
      <transition name="fade-slide" mode="out-in">
        <section v-if="currentPage === 'home'" key="home" class="screen">
          <div class="top-badge">💖 约会邀请</div>

          <div class="avatar-wrap">
            <div class="dog-avatar">🐶</div>
            <span class="sparkle sparkle-one">✨</span>
            <span class="sparkle sparkle-two">⭐</span>
            <span class="heart heart-one">❤</span>
          </div>

          <h1>可以和我一起约会嘛？！</h1>

          <p v-if="showLoveReply" class="reply-text">
            等下，你真的点了愿意？我都已经准备好被你点“不要”了。
          </p>

          <div class="choice-area">
            <button
              class="primary-btn home-primary"
              @click="handleYes"
            >
              愿意
            </button>

            <button
              class="ghost-btn"
              :style="{ left: `${noButtonPos.x}%`, top: `${noButtonPos.y}%` }"
              @click="moveNoButton"
            >
              不要
            </button>

            <button v-if="showLoveReply" class="confirm-btn" @click="goToTime">
              好哦好哦～
            </button>
          </div>
        </section>

        <section v-else-if="currentPage === 'time'" key="time" class="screen">
          <div class="mini-avatar">🐶</div>
          <h2>所以...你什么时候有空？</h2>

          <div class="form-card">
            <label class="field">
              <span>日期</span>
              <input v-model="selectedDate" type="date" />
            </label>

            <label class="field">
              <span>时间</span>
              <select v-model="selectedTime">
                <option v-for="slot in timeSlots" :key="slot" :value="slot">
                  {{ slot }}
                </option>
              </select>
            </label>

            <button class="primary-btn full-btn" @click="goToFood">确定时间</button>
          </div>
        </section>

        <section v-else-if="currentPage === 'food'" key="food" class="screen">
          <div class="mini-avatar">🐶</div>
          <h2>我们吃点什么？</h2>

          <div class="form-card food-card">
            <div class="food-grid">
              <button
                v-for="food in foodOptions"
                :key="food"
                class="food-chip"
                :class="{ selected: selectedFoods.includes(food) }"
                @click="toggleFood(food)"
              >
                {{ food }}
              </button>
            </div>

            <button class="primary-btn full-btn" :disabled="selectedFoods.length === 0" @click="goToResult">
              确认选择
            </button>
          </div>
        </section>

        <section v-else key="result" class="screen result-screen">
          <div class="result-avatar">🐶</div>
          <h2>真开心你没有拒绝——我会准时来接你！</h2>

          <div class="summary-card">
            <div class="summary-row">
              <span>日期</span>
              <strong>{{ formattedDate }}</strong>
            </div>
            <div class="summary-row">
              <span>时间</span>
              <strong>{{ selectedTime }}</strong>
            </div>
            <div class="summary-row">
              <span>餐饮</span>
              <strong>{{ selectedFoods.join('、') || '还没想好' }}</strong>
            </div>
          </div>

          <div class="footer-line">带好胃口，我带好路线。</div>
        </section>
      </transition>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import './App.css'

type PageKey = 'home' | 'time' | 'food' | 'result'

const currentPage = ref<PageKey>('home')
const showLoveReply = ref(false)
const selectedDate = ref(getTodayString())
const selectedTime = ref('15:00')
const selectedFoods = ref<string[]>(['披萨'])
const noButtonPos = ref({ x: 58, y: 18 })

const timeSlots = Array.from({ length: 7 }, (_, index) => {
  const hour = 12 + index
  return `${String(hour).padStart(2, '0')}:00`
})

const foodOptions = ['披萨', '寿司', '火锅', '烤肉', '早茶', '拉面', '麻辣烫', '小龙虾', '烧烤', '其他']

const formattedDate = computed(() => {
  const date = new Date(selectedDate.value)
  if (Number.isNaN(date.getTime())) return selectedDate.value

  return new Intl.DateTimeFormat('zh-CN', {
    month: 'numeric',
    day: 'numeric',
    weekday: 'short',
  }).format(date)
})

function getTodayString() {
  const date = new Date()
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

function moveNoButton() {
  noButtonPos.value = {
    x: 8 + Math.random() * 70,
    y: 8 + Math.random() * 52,
  }
}

function handleYes() {
  showLoveReply.value = true
}

function goToTime() {
  currentPage.value = 'time'
}

function goToFood() {
  currentPage.value = 'food'
}

function goToResult() {
  currentPage.value = 'result'
}

function toggleFood(food: string) {
  const index = selectedFoods.value.indexOf(food)

  if (index === -1) {
    selectedFoods.value = [...selectedFoods.value, food]
    return
  }

  selectedFoods.value = selectedFoods.value.filter((item) => item !== food)
}
</script>

