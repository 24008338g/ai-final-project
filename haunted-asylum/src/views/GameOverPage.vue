<template>
  <div class="gameover-container">
    <div class="gameover-content">
      <h1 class="gameover-title">GAME OVER</h1>
      
      <div class="media-container">
        <video 
          :src="`/${currentScene.id}.mp4`" 
          controls 
          autoplay
          class="scene-video"
        ></video>
      </div>
      
      <div class="description">
        <p>{{ currentScene.description }}</p>
      </div>
      
      <div class="actions">
        <button @click="restartGame" class="action-btn">Try Again</button>
        <button @click="returnToStart" class="action-btn">Main Menu</button>
      </div>
    </div>
  </div>
</template>

<script>
import { useRoute, useRouter } from 'vue-router'
import { narrative } from '../data/narrative'

export default {
  name: 'GameOverPage',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const currentScene = narrative.scenes.find(scene => scene.id === route.params.id)
    
    const restartGame = () => {
      router.push('/checkpoint/checkpoint1')
    }
    
    const returnToStart = () => {
      router.push('/')
    }
    
    return {
      currentScene,
      restartGame,
      returnToStart
    }
  }
}
</script>

<style scoped>
.gameover-container {
  min-height: 100vh;
  padding: 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(rgba(0, 0, 0, 0.9), rgba(50, 0, 0, 0.8));
}

.gameover-content {
  max-width: 700px;
  text-align: center;
  background: rgba(20, 0, 0, 0.9);
  padding: 3rem;
  border: 2px solid #8a1a1a;
  box-shadow: 0 0 40px rgba(255, 0, 0, 0.5);
}

.gameover-title {
  color: #8a1a1a;
  font-size: 4rem;
  margin-bottom: 2rem;
  text-shadow: 0 0 20px rgba(255, 0, 0, 0.7);
  font-family: 'Cinzel Decorative', cursive;
}

.media-container {
  margin-bottom: 2rem;
}

.scene-image {
  width: 100%;
  height: 250px;
  object-fit: cover;
  border: 2px solid #5a1a1a;
}

.scene-video {
  width: 100%;
  height: 250px;
  object-fit: cover;
  border: 2px solid #5a1a1a;
}

.description {
  margin-bottom: 3rem;
  line-height: 1.6;
  font-size: 1.1rem;
  color: #c0c0c0;
}

.actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.action-btn {
  background: linear-gradient(145deg, #3a0a0a, #2a0000);
  color: #c0c0c0;
  border: 1px solid #8a1a1a;
  padding: 0.8rem 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn:hover {
  background: linear-gradient(145deg, #4a1a1a, #3a0a0a);
  text-shadow: 0 0 10px rgba(255, 0, 0, 0.7);
  box-shadow: 0 0 15px rgba(255, 0, 0, 0.4);
}
</style>