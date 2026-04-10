/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Skull, Ghost, DoorOpen, ArrowRight, RotateCcw, Zap } from 'lucide-react';

type GameState = 'TITLE' | 'OPENING' | 'CHOICE_1' | 'TREATMENT_ROOM' | 'HALLWAY' | 'SUCCESS' | 'DEATH';

export default function App() {
  const [gameState, setGameState] = useState<GameState>('TITLE');
  const [deathReason, setDeathReason] = useState<string>("");

  // Preload fonts
  useEffect(() => {
    const link = document.createElement('link');
    link.href = 'https://fonts.googleapis.com/css2?family=Creepster&family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;600&display=swap';
    link.rel = 'stylesheet';
    document.head.appendChild(link);
  }, []);

  const handleChoice = (nextState: GameState, reason?: string) => {
    if (reason) setDeathReason(reason);
    setGameState(nextState);
  };

  const resetGame = () => {
    setGameState('TITLE');
    setDeathReason("");
  };

  return (
    <div className="relative w-full h-screen overflow-hidden bg-black font-sans selection:bg-red-900 selection:text-white">
      <AnimatePresence mode="wait">
        {gameState === 'TITLE' && (
          <TitleScreen onStart={() => setGameState('OPENING')} />
        )}
        {gameState === 'OPENING' && (
          <StoryScreen
            title="OPENING"
            text="Dr. Elara Valois stands in the decaying central hall of Shadowbrook's abandoned asylum wing. The air is thick with dust and the scent of ozone. Flickering lights reveal The Faceless One standing at the far end of the hall – their face a shifting, purple holographic void. Patient files and medical equipment float around them in a chaotic 'Your data will complete the collection,' they whisper in a chorus of stolen voices. Elara must survive this confrontation and uncover the truth behind the asylum's experiments."
            image="https://picsum.photos/seed/asylum-hall/1920/1080?blur=2"
            onContinue={() => setGameState('CHOICE_1')}
          />
        )}
        {gameState === 'CHOICE_1' && (
          <ChoiceScreen
            image="https://picsum.photos/seed/asylum-horror/1920/1080"
            choices={[
              {
                text: "Duck into a treatment room",
                action: () => handleChoice('TREATMENT_ROOM')
              },
              {
                text: "Push past them down the hallway",
                action: () => handleChoice('DEATH', "The Faceless One's void consumed you as you tried to run past. The asylum claims another soul.")
              }
            ]}
          />
        )}
        {gameState === 'TREATMENT_ROOM' && (
          <StoryScreen
            title="THE ROOM"
            text="The treatment room is cold, filled with rusted surgical tools and the faint sound of static. You find a hidden lever behind a loose wall panel. It seems to lead to a secret exit, but the sound of heavy footsteps is approaching fast from the hallway."
            image="https://picsum.photos/seed/asylum-room/1920/1080?grayscale"
            onContinue={() => setGameState('SUCCESS')}
          />
        )}
        {gameState === 'SUCCESS' && (
          <EndingScreen onReset={resetGame} />
        )}
        {gameState === 'DEATH' && (
          <GameOverScreen reason={deathReason} onReset={resetGame} />
        )}
      </AnimatePresence>

      {/* Atmospheric Overlays */}
      <div className="pointer-events-none fixed inset-0 z-50">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,transparent_0%,rgba(0,0,0,0.4)_100%)]" />
        <div className="absolute inset-0 opacity-[0.03] bg-[url('https://www.transparenttextures.com/patterns/stardust.png')]" />
      </div>
    </div>
  );
}

function TitleScreen({ onStart }: { onStart: () => void }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="relative w-full h-full flex flex-col items-center justify-center bg-[url('https://picsum.photos/seed/asylum-hallway/1920/1080?blur=4')] bg-cover bg-center"
    >
      <div className="absolute inset-0 bg-black/60" />
      
      <motion.div
        initial={{ y: -50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.5, duration: 1 }}
        className="relative z-10 text-center"
      >
        <h1 className="font-horror text-7xl md:text-9xl text-red-600 drop-shadow-[0_0_15px_rgba(220,38,38,0.8)] tracking-wider mb-2">
          HAUNTED ASYLUM
        </h1>
        <h2 className="font-serif italic text-2xl md:text-3xl text-gray-300 tracking-widest mb-12">
          The Shadowbrook Chronicles
        </h2>

        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={onStart}
          className="group relative px-12 py-4 bg-red-900/80 border-2 border-red-600 text-white font-bold text-2xl tracking-widest uppercase horror-glow transition-all duration-300"
        >
          <span className="relative z-10">Begin Your Nightmare</span>
          <div className="absolute inset-0 bg-red-600 opacity-0 group-hover:opacity-20 transition-opacity" />
        </motion.button>
      </motion.div>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 0.6 }}
        transition={{ delay: 1.5 }}
        className="absolute bottom-12 font-serif italic text-gray-400 text-lg"
      >
        Your choices determine your fate...
      </motion.p>
    </motion.div>
  );
}

function StoryScreen({ title, text, image, onContinue }: { title: string, text: string, image: string, onContinue: () => void }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="relative w-full h-full flex items-center justify-center bg-cover bg-center"
      style={{ backgroundImage: `url(${image})` }}
    >
      <div className="absolute inset-0 bg-black/40 backdrop-blur-sm" />
      
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        className="relative z-10 max-w-2xl w-full mx-4 p-8 md:p-12 bg-black/80 border border-gray-800 rounded-lg backdrop-blur-md shadow-2xl"
      >
        <h2 className="font-horror text-4xl text-red-600 mb-8 text-center tracking-widest uppercase">
          {title}
        </h2>
        
        <p className="text-gray-300 text-lg md:text-xl leading-relaxed font-serif mb-12 first-letter:text-4xl first-letter:font-horror first-letter:text-red-600 first-letter:mr-2 first-letter:float-left">
          {text}
        </p>

        <div className="flex justify-center">
          <button
            onClick={onContinue}
            className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors tracking-[0.2em] uppercase text-sm font-semibold group"
          >
            Continue <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </button>
        </div>
      </motion.div>
    </motion.div>
  );
}

function ChoiceScreen({ image, choices }: { image: string, choices: { text: string, action: () => void }[] }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="relative w-full h-full flex flex-col items-center justify-end pb-24 bg-cover bg-center"
      style={{ backgroundImage: `url(${image})` }}
    >
      <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-black/40" />
      
      <div className="relative z-10 w-full max-w-xl px-6 space-y-4">
        {choices.map((choice, idx) => (
          <motion.button
            key={idx}
            initial={{ x: -20, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ delay: idx * 0.2 }}
            whileHover={{ scale: 1.02, x: 10 }}
            onClick={choice.action}
            className="w-full p-4 bg-black/60 border border-red-900/50 hover:border-red-600 text-gray-200 hover:text-white text-lg md:text-xl font-serif italic transition-all duration-300 text-left pl-8 relative group"
          >
            <div className="absolute left-0 top-0 bottom-0 w-1 bg-red-900 group-hover:bg-red-600 transition-colors" />
            {choice.text}
          </motion.button>
        ))}
      </div>
    </motion.div>
  );
}

function EndingScreen({ onReset }: { onReset: () => void }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="relative w-full h-full flex flex-col items-center justify-center bg-[url('https://picsum.photos/seed/asylum-gate/1920/1080')] bg-cover bg-center"
    >
      <div className="absolute inset-0 bg-black/40" />
      
      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        className="relative z-10 text-center"
      >
        <h1 className="font-serif text-5xl md:text-7xl text-white tracking-widest mb-12 uppercase">
          The Cycle is Broken
        </h1>

        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={onReset}
          className="px-10 py-3 border border-white text-white uppercase tracking-[0.3em] text-sm hover:bg-white hover:text-black transition-all duration-500"
        >
          Awaken
        </motion.button>
      </motion.div>
    </motion.div>
  );
}

function GameOverScreen({ reason, onReset }: { reason: string, onReset: () => void }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="relative w-full h-full flex flex-col items-center justify-center bg-black"
    >
      {/* Glitchy silhouette background */}
      <div className="absolute inset-0 opacity-20 flex items-center justify-center overflow-hidden">
        <motion.div
          animate={{ 
            scale: [1, 1.1, 1],
            opacity: [0.2, 0.4, 0.2],
            x: [0, 5, -5, 0]
          }}
          transition={{ duration: 0.2, repeat: Infinity }}
        >
          <Ghost className="w-[80vh] h-[80vh] text-red-900" />
        </motion.div>
      </div>

      <div className="relative z-10 text-center px-6">
        <p className="text-gray-500 uppercase tracking-[0.4em] text-xs mb-8">
          Haunted Asylum: The Shadowbrook Chronicles
        </p>
        
        <h1 className="glitch-text font-horror text-8xl md:text-9xl text-white mb-12 tracking-tighter">
          YOU PERISHED
        </h1>

        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={onReset}
          className="px-8 py-3 bg-white/10 border border-white/20 hover:bg-white hover:text-black text-white uppercase tracking-[0.2em] text-sm transition-all duration-300 mb-12"
        >
          Return to Main Menu
        </motion.button>

        <p className="font-mono text-gray-500 text-sm max-w-md mx-auto leading-relaxed">
          {reason || "Your journey ends here. The asylum claims another soul."}
        </p>
      </div>

      {/* Static effect */}
      <div className="absolute inset-0 pointer-events-none opacity-10 bg-[url('https://media.giphy.com/media/oEI9uWUqnW3Fe/giphy.gif')] bg-cover" />
    </motion.div>
  );
}
