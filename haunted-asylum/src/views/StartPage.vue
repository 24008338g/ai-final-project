<template>
  <div class="start-container" :style="{ backgroundImage: 'url(/title_screen.png)' }">
    <button @click="startGame" class="start-button horror-glow">
      BEGIN YOUR NIGHTMARE
    </button>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'

export default {
  name: 'StartPage',
  setup() {
    const router = useRouter()
    
    const startGame = () => {
      router.push('/cinematic/opening')
    }
    
    return {
      startGame
    }
  }
}
</script>

<style scoped>
.start-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  text-align: center;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  position: relative;
}

.start-button {
  position: relative;
  z-index: 10;
}


.start-button {
  background: rgba(153, 27, 27, 0.8);
  color: #ffffff;
  border: 2px solid #dc2626;
  padding: 1rem 2rem;
  font-size: 1.2rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.1rem;
  font-weight: bold;
  position: relative;
  overflow: hidden;
}

.start-button::before {
  content: '';
  position: absolute;
  inset: 0;
  background: #dc2626;
  opacity: 0;
  transition: opacity 0.3s;
}

.start-button:hover::before {
  opacity: 0.2;
}

.start-button:hover {
  box-shadow: 0 0 25px rgba(255, 0, 0, 0.8);
}
</style>