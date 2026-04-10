<template>
  <div class="cinematic-container">
    <div class="scene-content">
      <h2 class="scene-title">{{ currentScene.id }}</h2>
      
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
      
      <div class="navigation">
        <button 
          v-if="nextScene" 
          @click="continueJourney" 
          class="continue-btn"
        >
          Continue
        </button>
        <button 
          v-else-if="currentScene.id === 'opening'" 
          @click="$router.push('/checkpoint/checkpoint1')" 
          class="continue-btn"
        >
          Proceed
        </button>
        <button 
          v-else-if="currentScene.id === 'true_ending'" 
          @click="$router.push('/')" 
          class="continue-btn"
        >
          Return to Home
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { useRoute, useRouter } from 'vue-router'
import { narrative } from '../data/narrative'

export default {
  name: 'CinematicPage',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const currentScene = narrative.scenes.find(scene => scene.id === route.params.id)
    
    const continueJourney = () => {
      if (currentScene.id === 'progress1') {
        router.push('/checkpoint/checkpoint2')
      } else if (currentScene.id === 'progress2') {
        router.push('/checkpoint/checkpoint3')
      }
    }
    
    const nextScene = currentScene.id === 'progress1' || currentScene.id === 'progress2'
    
    return {
      currentScene,
      nextScene,
      continueJourney
    }
  }
}
</script>

<style scoped>
.cinematic-container {
  min-height: 100vh;
  padding: 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.scene-content {
  max-width: 800px;
  background: rgba(20, 10, 20, 0.8);
  padding: 2rem;
  border: 1px solid #5a1a1a;
  box-shadow: 0 0 30px rgba(139, 0, 0, 0.4);
}

.scene-title {
  color: #8a1a1a;
  text-align: center;
  margin-bottom: 2rem;
  font-family: 'Cinzel Decorative', cursive;
  text-transform: uppercase;
}

.media-container {
  margin-bottom: 2rem;
}

.scene-video {
  width: 100%;
  height: 400px;
  object-fit: cover;
  border: 2px solid #5a1a1a;
}

.description {
  margin-bottom: 2rem;
  line-height: 1.6;
  font-size: 1.1rem;
}

.continue-btn {
  background: linear-gradient(145deg, #2a0a0a, #1a0000);
  color: #c0c0c0;
  border: 1px solid #8a1a1a;
  padding: 0.8rem 2rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: block;
  margin: 0 auto;
}

.continue-btn:hover {
  background: linear-gradient(145deg, #3a1a1a, #2a0a0a);
  text-shadow: 0 0 10px rgba(255, 0, 0, 0.7);
  box-shadow: 0 0 15px rgba(255, 0, 0, 0.4);
}
</style>