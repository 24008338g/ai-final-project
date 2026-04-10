<template>
  <div class="cinematic-container">
    <div class="scene-content">
      
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
  name: 'CinematicPage',
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
.cinematic-container {
  min-height: 100vh;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.scene-content {
  position: relative;
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
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
</style>