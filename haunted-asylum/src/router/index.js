import { createRouter, createWebHistory } from 'vue-router'
import StartPage from '../views/StartPage.vue'
import CinematicPage from '../views/CinematicPage.vue'
import CheckpointPage from '../views/CheckpointPage.vue'
import GameOverPage from '../views/GameOverPage.vue'
import TrueEndingPage from '../views/TrueEndingPage.vue'

const routes = [
  { path: '/', name: 'start', component: StartPage },
  { path: '/cinematic/:id', name: 'cinematic', component: CinematicPage },
  { path: '/checkpoint/:id', name: 'checkpoint', component: CheckpointPage },
  { path: '/game-over/:id', name: 'game-over', component: GameOverPage },
  { path: '/true-ending', name: 'true-ending', component: TrueEndingPage }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router