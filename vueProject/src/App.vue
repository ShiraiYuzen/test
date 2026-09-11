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
            <div class="action-row">
              <button class="primary-btn action-btn" @click="handleYes">
                愿意
              </button>

              <button
                class="ghost-btn action-btn"
                :style="{ left: `${noButtonPos.x}%`, top: `${noButtonPos.y}%` }"
                @click="moveNoButton"
              >
                不要
              </button>
            </div>

            <button v-if="showLoveReply" class="confirm-btn" @click="goToTime">
              好眼好哦～
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

<style scoped>
.app-shell {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(180deg, #f9d7ef 0%, #f9e0ff 34%, #f6ecff 100%);
  padding: 20px 14px;
}

.phone-frame {
  width: min(100%, 420px);
  min-height: 760px;
  border-radius: 34px;
  background: rgba(255, 255, 255, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.7);
  box-shadow: 0 18px 38px rgba(155, 92, 186, 0.18);
  padding: 14px;
  backdrop-filter: blur(8px);
}

.screen {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 730px;
  background: rgba(255, 255, 255, 0.62);
  border-radius: 28px;
  padding: 24px 18px 18px;
  overflow: hidden;
}

.top-badge,
.mini-avatar,
.result-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: linear-gradient(135deg, #ffd9eb 0%, #f7d8ff 100%);
  box-shadow: 0 12px 24px rgba(214, 108, 180, 0.18);
  font-size: 32px;
}

.top-badge {
  width: auto;
  height: auto;
  border-radius: 999px;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 700;
  color: #c7568d;
  background: rgba(255, 255, 255, 0.7);
  box-shadow: 0 10px 18px rgba(194, 110, 171, 0.12);
}

.avatar-wrap {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 160px;
  height: 160px;
  margin-top: 18px;
  margin-bottom: 18px;
  border-radius: 50%;
  background: linear-gradient(135deg, #ffd7f0 0%, #f8d5ff 100%);
  box-shadow: 0 18px 30px rgba(216, 116, 196, 0.2);
}

.dog-avatar {
  font-size: 86px;
  filter: drop-shadow(0 10px 14px rgba(177, 105, 184, 0.2));
}

.sparkle,
.heart {
  position: absolute;
  font-size: 22px;
  animation: float 2.5s ease-in-out infinite alternate;
}

.sparkle-one {
  top: 18px;
  right: 18px;
}

.sparkle-two {
  bottom: 18px;
  left: 18px;
}

.heart-one {
  right: 26px;
  bottom: 32px;
  color: #ff7ab4;
}

h1,
h2 {
  margin: 0;
  text-align: center;
  color: #5b2a5a;
  line-height: 1.3;
}

h1 {
  font-size: clamp(2rem, 5vw, 2.5rem);
  margin-top: 6px;
}

h2 {
  margin-top: 16px;
  font-size: clamp(1.7rem, 4vw, 2rem);
}

.reply-text {
  margin: 18px 0 0;
  padding: 12px 14px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.7);
  color: #d763a2;
  font-size: 0.95rem;
  text-align: center;
  line-height: 1.6;
  box-shadow: 0 10px 22px rgba(201, 119, 176, 0.12);
}

.choice-area {
  position: relative;
  width: 100%;
  margin-top: 18px;
}

.action-row {
  position: relative;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
  width: 100%;
  min-height: 120px;
}

.primary-btn,
.ghost-btn,
.confirm-btn,
.food-chip {
  border: none;
  transition: transform 0.2s ease, box-shadow 0.2s ease, opacity 0.2s ease;
}

.primary-btn:active,
.ghost-btn:active,
.confirm-btn:active,
.food-chip:active {
  transform: scale(0.97);
}

.action-btn {
  min-width: 0;
  height: 54px;
  border-radius: 18px;
  font-weight: 700;
  font-size: 1.08rem;
}

.primary-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #ff7fb7 0%, #f85aa6 100%);
  color: white;
  box-shadow: 0 10px 20px rgba(249, 112, 163, 0.28);
}

.confirm-btn {
  width: 100%;
  margin-top: 18px;
  background: linear-gradient(135deg, #f4b2d9 0%, #d98ad7 100%);
  color: #fff;
  height: 54px;
  border-radius: 18px;
  font-weight: 700;
  font-size: 1.08rem;
  box-shadow: 0 10px 20px rgba(212, 119, 204, 0.22);
}

.ghost-btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 0 18px;
  background: rgba(255, 255, 255, 0.9);
  color: #d56ab1;
  box-shadow: 0 10px 18px rgba(201, 124, 179, 0.12);
  border: 1px solid rgba(240, 168, 213, 0.8);
  font-size: 1rem;
}

.form-card {
  width: 100%;
  margin-top: 26px;
  padding: 20px 18px 18px;
  border-radius: 26px;
  background: rgba(255, 255, 255, 0.72);
  box-shadow: 0 16px 22px rgba(196, 126, 179, 0.12);
}

.field {
  display: grid;
  gap: 10px;
  margin-bottom: 18px;
}

.field span {
  color: #69366b;
  font-size: 0.95rem;
  font-weight: 700;
}

input,
select {
  width: 100%;
  min-height: 52px;
  border: 1px solid #f4d8eb;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.9);
  padding: 0 16px;
  font-size: 1rem;
  color: #4d2d4d;
  outline: none;
  box-shadow: inset 0 1px 2px rgba(185, 124, 180, 0.04);
}

.full-btn {
  width: 100%;
  margin-top: 8px;
}

.food-card {
  padding-top: 18px;
}

.food-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 20px;
}

.food-chip {
  min-height: 52px;
  border-radius: 16px;
  padding: 12px 10px;
  background: rgba(255, 255, 255, 0.9);
  color: #714873;
  font-weight: 700;
  border: 1px solid rgba(236, 169, 210, 0.7);
}

.food-chip.selected {
  background: linear-gradient(135deg, #ffb3d3 0%, #f884ba 100%);
  color: white;
  border-color: transparent;
  box-shadow: 0 10px 18px rgba(248, 132, 186, 0.2);
}

.result-screen {
  justify-content: center;
}

.result-avatar {
  width: 110px;
  height: 110px;
  font-size: 52px;
}

.summary-card {
  width: 100%;
  margin-top: 26px;
  padding: 18px 16px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.8);
  box-shadow: 0 12px 22px rgba(194, 119, 200, 0.12);
}

.summary-row {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px dashed rgba(202, 140, 178, 0.4);
  color: #804d79;
}

.summary-row:last-child {
  border-bottom: none;
}

.summary-row span {
  font-weight: 700;
}

.summary-row strong {
  text-align: right;
  line-height: 1.5;
  color: #5b2a5a;
}

.footer-line {
  width: 100%;
  margin-top: 22px;
  text-align: center;
  color: #d15a9b;
  font-weight: 800;
  letter-spacing: 0.04em;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.28s ease;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(12px) scale(0.98);
}

.fade-slide-enter-to,
.fade-slide-leave-from {
  opacity: 1;
  transform: translateY(0) scale(1);
}

@keyframes float {
  0% {
    transform: translateY(0px) scale(1);
  }
  100% {
    transform: translateY(-6px) scale(1.05);
  }
}
</style>
