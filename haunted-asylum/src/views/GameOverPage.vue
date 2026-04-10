<template>
  <div class="gameover-container" :style="{ backgroundImage: 'url(/game_over_screen.png)' }">
    <div class="gameover-content">
      
      <div class="media-container">
        <video 
          :src="`/${currentScene.id}.mp4`" 
          controls 
          autoplay
          @ended="onVideoEnd"
          class="scene-video"
        ></video>
      </div>
    </div>
    
    <div v-if="fading" class="fade-overlay"></div>
  </div>
</template>

<script>
import { useRoute, useRouter } from 'vue-router'
import { ref } from 'vue'
import { narrative } from '../data/narrative'

export default {
  name: 'GameOverPage',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const currentScene = narrative.scenes.find(scene => scene.id === route.params.id)
    
    let fading = ref(false)
    
    const onVideoEnd = () => {
      fading.value = true
      setTimeout(() => {
        router.push(`/narrative/${currentScene.id}`)
      }, 1000)
    }
    
    return {
      currentScene,
      fading,
      onVideoEnd
    }
  }
}
</script>

<style scoped>
.gameover-container {
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

.gameover-container::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.8));
  pointer-events: none;
}

.gameover-content {
  position: relative;
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: rgba(20, 0, 0, 0.9);
}

.media-container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.scene-video {
  width: 100vw;
  height: 100vh;
  object-fit: cover;
}

.fade-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: black;
  opacity: 1;
  transition: opacity 1s ease;
  z-index: 1000;
}
</style>