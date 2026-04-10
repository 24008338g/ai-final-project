<template>
  <div class="checkpoint-container" :style="{ backgroundImage: `url(/${currentScene.id}.png)` }">
    <div class="situation">
      <p class="font-serif text-lg md:text-xl leading-relaxed italic text-left pl-8 relative">
        <span class="absolute left-0 top-0 bottom-0 w-1 bg-red-900"></span>
        {{ currentScene.description }}
      </p>
    </div>
    
    <div class="choices">
      <button 
        v-for="(choice, index) in currentScene.choices" 
        :key="index" 
        @click="makeChoice(choice)"
        class="choice-btn"
      >
        <div class="absolute left-0 top-0 bottom-0 w-1 bg-red-900 group-hover:bg-red-600 transition-colors"></div>
        {{ choice.text }}
      </button>
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
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding-bottom: 2rem;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  position: relative;
}

.checkpoint-container::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 1) 0%, transparent 40%, rgba(0, 0, 0, 0.4) 100%);
}

.situation {
  position: absolute;
  top: 2rem;
  left: 2rem;
  right: 2rem;
  z-index: 10;
}

.situation p {
  background: rgba(0, 0, 0, 0.6);
  border: 1px solid rgba(220, 38, 38, 0.5);
  padding: 1rem;
  border-radius: 4px;
  color: #d1d5db;
  font-style: italic;
  position: relative;
}

.choices {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 40rem;
  margin: 0 auto;
  padding: 0 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.choice-btn {
  width: 100%;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.6);
  border: 1px solid rgba(220, 38, 38, 0.5);
  color: #d1d5db;
  text-align: left;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Playfair Display', serif;
  font-style: italic;
  font-size: 1.125rem;
  position: relative;
  padding-left: 2rem;
}

.choice-btn::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: #7f1d1d;
  transition: background-color 0.3s;
}

.choice-btn:hover::before {
  background: #dc2626;
}

.choice-btn:hover {
  background: rgba(220, 38, 38, 0.1);
  color: #ffffff;
  border-color: #dc2626;
  transform: translateX(10px);
}
</style>