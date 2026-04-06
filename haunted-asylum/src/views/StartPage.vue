<template>
  <div class="start-container">
    <div class="title-section">
      <h1>HAUNTED ASYLUM</h1>
      <h2>The Shadowbrook Chronicles</h2>
    </div>
    
    <div class="intro-section">
      <p>Enter the decaying halls of Shadowbrook Asylum...</p>
    </div>
    
    <button @click="startGame" class="start-button">BEGIN YOUR NIGHTMARE</button>
    
    <div class="footer">
      <p>Your choices determine your fate...</p>
    </div>
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
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  padding: 2rem;
  text-align: center;
}

.title-section h1 {
  font-size: 4rem;
  color: #8a1a1a;
  text-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
  margin-bottom: 1rem;
  font-family: 'Cinzel Decorative', cursive;
}

.title-section h2 {
  font-size: 1.5rem;
  color: #c0c0c0;
  letter-spacing: 0.3rem;
}

.intro-section {
  margin: 2rem 0;
}

.intro-section p {
  font-size: 1.2rem;
  margin-bottom: 1.5rem;
  color: #d0d0d0;
}

.start-button {
  background: linear-gradient(145deg, #2a0a0a, #1a0000);
  color: #c0c0c0;
  border: 2px solid #8a1a1a;
  padding: 1rem 2rem;
  font-size: 1.2rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.1rem;
}

.start-button:hover {
  background: linear-gradient(145deg, #3a1a1a, #2a0a0a);
  text-shadow: 0 0 10px rgba(255, 0, 0, 0.7);
  box-shadow: 0 0 20px rgba(255, 0, 0, 0.4);
}

.footer {
  margin-top: 2rem;
  color: #666;
}
</style>