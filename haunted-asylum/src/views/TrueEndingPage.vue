<template>
  <div class="ending-container" :style="{ backgroundImage: 'url(/true_ending_screen.png)' }">
    <button @click="returnToStart" class="return-btn horror-glow">
      RETURN TO HOME
    </button>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'

export default {
  name: 'TrueEndingPage',
  setup() {
    const router = useRouter()

    const returnToStart = () => {
      router.push('/')
    }

    return {
      returnToStart
    }
  }
}
</script>

<style scoped>
.ending-container {
  min-height: 100vh;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.return-btn {
  background: rgba(153, 27, 27, 0.85);
  color: #ffffff;
  border: 2px solid #dc2626;
  padding: 1rem 2rem;
  font-size: 1.2rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.1rem;
  font-weight: bold;
  z-index: 10;
}

.return-btn:hover {
  box-shadow: 0 0 25px rgba(255, 0, 0, 0.8);
}
</style>