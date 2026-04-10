<template>
  <div class="narrative-container" :style="backgroundStyle">
    <div class="scene-content" :class="{ 'ending-scene': currentScene.id === 'true_ending' }">
      <div v-if="currentScene.id === 'true_ending'" class="ending-content">
        <h1 class="ending-title font-serif text-5xl md:text-7xl text-white tracking-widest mb-8 uppercase">
          The Cycle is Broken
        </h1>
        <p class="ending-description text-lg md:text-xl text-gray-200 max-w-3xl mx-auto mb-12">
          {{ currentScene.description }}
        </p>
        <button @click="returnToStart" class="continue-btn">
          Return to Home
        </button>
      </div>
      <div v-else>
        <h2 class="scene-title font-horror text-4xl text-red-600 mb-8 text-center tracking-widest uppercase">
          {{ currentScene.id.startsWith('game_over') ? 'Game Over' : currentScene.id }}
        </h2>
        <div class="description font-serif text-lg md:text-xl leading-relaxed mb-12 first-letter:text-4xl first-letter:font-horror first-letter:text-red-600 first-letter:mr-2 first-letter:float-left">
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
          <div v-else-if="isGameOver" class="game-over-actions">
            <button @click="restartGame" class="action-btn">Try Again</button>
            <button @click="returnToStart" class="action-btn">Main Menu</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useRoute, useRouter } from 'vue-router'
import { narrative } from '../data/narrative'

export default {
  name: 'NarrativePage',
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

    const isGameOver = currentScene.id.startsWith('game_over')

    const restartGame = () => {
      router.push('/checkpoint/checkpoint1')
    }

    const returnToStart = () => {
      router.push('/')
    }

    const backgroundStyle = {
      backgroundImage: currentScene.id === 'true_ending'
        ? "url('/true_ending_screen.png')"
        : currentScene.id.startsWith('game_over')
          ? "url('/game_over_screen.png')"
          : "url('/placeholder_image.jpg')"
    }

    return {
      currentScene,
      nextScene,
      continueJourney,
      isGameOver,
      restartGame,
      returnToStart,
      backgroundStyle
    }
  }
}
</script>

<style scoped>
.narrative-container {
  min-height: 100vh;
  padding: 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
  background: center/cover no-repeat;
  position: relative;
}

.narrative-container::before {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);
}

.scene-content {
  max-width: 800px;
  width: 100%;
  background: rgba(0, 0, 0, 0.8);
  border: 1px solid rgba(156, 163, 175, 0.3);
  padding: 2rem;
  border-radius: 8px;
  backdrop-filter: blur(8px);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  position: relative;
  z-index: 10;
}

.scene-content.ending-scene {
  max-width: 900px;
  background: rgba(0, 0, 0, 0.75);
  padding: 3rem;
}

.scene-title {
  color: #dc2626;
  margin-bottom: 2rem;
  text-transform: uppercase;
  letter-spacing: 0.2rem;
}

.ending-content {
  text-align: center;
}

.ending-title {
  color: #ffffff;
  margin-bottom: 3rem;
}

.ending-description {
  margin-bottom: 12px;
}

.description {
  margin-bottom: 2rem;
  line-height: 1.6;
  color: #d1d5db;
}

.description p::first-letter {
  font-size: 2.5rem;
  color: #dc2626;
  font-family: 'Creepster', cursive;
  margin-right: 0.5rem;
  float: left;
}

.credits {
  text-align: center;
  padding: 1rem;
  border-top: 1px solid rgba(156, 163, 175, 0.3);
  border-bottom: 1px solid rgba(156, 163, 175, 0.3);
  margin-bottom: 2rem;
}

.credits h3 {
  color: #d1d5db;
  margin-bottom: 0.5rem;
  font-family: 'Playfair Display', serif;
}

.credits p {
  font-style: italic;
  color: #9ca3af;
}

.continue-btn {
  background: rgba(0, 0, 0, 0.6);
  color: #9ca3af;
  border: 1px solid rgba(220, 38, 38, 0.5);
  padding: 0.8rem 2rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: block;
  margin: 0 auto;
  text-transform: uppercase;
  letter-spacing: 0.1rem;
  font-weight: 600;
}

.continue-btn:hover {
  background: rgba(220, 38, 38, 0.1);
  color: #ffffff;
  border-color: #dc2626;
}

.game-over-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.action-btn {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 0.8rem 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.1rem;
  font-size: 0.875rem;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.9);
  color: #000000;
}
</style>