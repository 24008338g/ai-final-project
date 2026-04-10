<template>
  <div class="ending-container">
    <div class="ending-content">
      <h1 class="ending-title">TRUE ENDING</h1>
      
      <div class="media-container">
        <video 
          src="/true_ending.mp4" 
          controls 
          autoplay
          class="scene-video"
        ></video>
      </div>
      
      <div class="description">
        <p>{{ currentScene.description }}</p>
      </div>
      
      <div class="credits">
        <h3>Thank you for playing</h3>
        <p>The horrors of Shadowbrook have been laid to rest...</p>
      </div>
      
      <button @click="returnToStart" class="return-btn">Return to Home</button>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import { narrative } from '../data/narrative'

export default {
  name: 'TrueEndingPage',
  setup() {
    const router = useRouter()
    
    const currentScene = narrative.scenes.find(scene => scene.id === 'true_ending')
    
    const returnToStart = () => {
      router.push('/')
    }
    
    return {
      currentScene,
      returnToStart
    }
  }
}
</script>

<style scoped>
.ending-container {
  min-height: 100vh;
  padding: 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 20, 20, 0.7));
}

.ending-content {
  max-width: 700px;
  text-align: center;
  background: rgba(10, 20, 20, 0.9);
  padding: 3rem;
  border: 2px solid #1a8a8a;
  box-shadow: 0 0 40px rgba(0, 139, 139, 0.5);
}

.ending-title {
  color: #1a8a8a;
  font-size: 3.5rem;
  margin-bottom: 2rem;
  text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
  font-family: 'Cinzel Decorative', cursive;
}

.media-container {
  margin-bottom: 2rem;
}

.scene-image {
  width: 100%;
  height: 300px;
  object-fit: cover;
  border: 2px solid #1a5a5a;
}

.scene-video {
  width: 100%;
  height: 300px;
  object-fit: cover;
  border: 2px solid #1a5a5a;
}

.description {
  margin-bottom: 2rem;
  line-height: 1.6;
  font-size: 1.1rem;
  color: #c0c0c0;
}

.credits {
  margin-bottom: 2rem;
  padding: 1rem;
  border-top: 1px solid #1a5a5a;
  border-bottom: 1px solid #1a5a5a;
}

.credits h3 {
  color: #1a8a8a;
  margin-bottom: 0.5rem;
}

.return-btn {
  background: linear-gradient(145deg, #0a2a2a, #002020);
  color: #c0c0c0;
  border: 1px solid #1a8a8a;
  padding: 0.8rem 2rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.return-btn:hover {
  background: linear-gradient(145deg, #1a3a3a, #0a2a2a);
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.7);
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.4);
}
</style>