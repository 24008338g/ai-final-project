<template>
  <div class="checkpoint-container">
    <div class="decision-content">
      <h2 class="checkpoint-title">DECISION POINT</h2>
      
      <div class="situation">
        <p>{{ currentScene.description }}</p>
      </div>
      
      <div class="media-container">
        <img 
          :src="`/${currentScene.id}.png`" 
          alt="Decision point" 
          class="scene-image"
        >
      </div>
      
      <div class="choices">
        <button 
          v-for="(choice, index) in currentScene.choices" 
          :key="index" 
          @click="makeChoice(choice)"
          class="choice-btn"
        >
          {{ choice.text }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { useRoute, useRouter } from 'vue-router'
import { narrative } from '../data/narrative'

export default {
  name: 'CheckpointPage',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const currentScene = narrative.scenes.find(scene => 
      scene.id === route.params.id && scene.type === 'checkpoint'
    )
    
    const makeChoice = (choice) => {
      if (choice.outcome === 'progress') {
        router.push(`/cinematic/${choice.cinematic}`)
      } else if (choice.outcome === 'game_over') {
        router.push(`/game-over/${choice.cinematic}`)
      }
    }
    
    return {
      currentScene,
      makeChoice
    }
  }
}
</script>

<style scoped>
.checkpoint-container {
  min-height: 100vh;
  padding: 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.decision-content {
  max-width: 800px;
  background: rgba(20, 10, 20, 0.8);
  padding: 2rem;
  border: 1px solid #5a1a1a;
  box-shadow: 0 0 30px rgba(139, 0, 0, 0.4);
}

.checkpoint-title {
  color: #8a1a1a;
  text-align: center;
  margin-bottom: 2rem;
  font-family: 'Cinzel Decorative', cursive;
  text-transform: uppercase;
  letter-spacing: 0.2rem;
}

.situation {
  margin-bottom: 2rem;
  line-height: 1.6;
  font-size: 1.1rem;
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

.choices {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.choice-btn {
  background: linear-gradient(145deg, #2a0a0a, #1a0000);
  color: #c0c0c0;
  border: 1px solid #8a1a1a;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
}

.choice-btn:hover {
  background: linear-gradient(145deg, #3a1a1a, #2a0a0a);
  text-shadow: 0 0 10px rgba(255, 0, 0, 0.7);
  box-shadow: 0 0 15px rgba(255, 0, 0, 0.4);
  transform: translateY(-2px);
}
</style>