@import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display&family=SF+Mono&display=swap');

html,body, .stApp {
  height: 100%;
  background: linear-gradient(135deg, rgba(12,18,40,0.9), rgba(8,12,25,0.94));
  overflow-y: scroll;
  font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
  color: #d0e4ff;
}

.glass-container {
  max-width: 1400px;
  margin: 3rem auto;
  padding: 3rem 4rem 4rem 4rem;
  border-radius: 38px;
  background: rgba(20, 30, 58, 0.36);
  box-shadow:
      inset 0 0 30px 0 rgba(64,160,255,0.3),
      0 15px 40px rgba(0, 0, 50, 0.65),
      0 0 60px 5px rgba(20, 45, 75, 0.9);
  border: 2.5px solid rgba(21, 31, 55, 0.45);
  position: relative;
  backdrop-filter: saturate(160%) blur(25px);
  -webkit-backdrop-filter: saturate(160%) blur(25px);
  animation: floatSlight 16s ease-in-out infinite;
}

@keyframes floatSlight {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px);}
}

.glass-container::before {
  content: "";
  position: absolute;
  pointer-events: none;
  top: 0; left: 0; right: 0; bottom: 0;
  border-radius: 38px;
  box-shadow:
    inset 0 0 25px 2px rgba(64, 160, 255, 0.3),
    0 0 45px 3px rgba(220, 180, 30, 0.15);
  animation: pulseGlow 15s ease-in-out infinite;
  z-index: 0;
}

@keyframes pulseGlow {
  0%, 100% { opacity: 0.8; }
  50% { opacity: 1; }
}

.glass-title {
  font-size: 4.2rem;
  font-weight: 900;
  letter-spacing: -0.05em;
  color: #b8d4ff;
  text-shadow:
    0 0 35px #2090ff,
    0 0 65px #ffd632,
    0 0 115px #ff4d3b;
  margin-bottom: 0.2rem;
  position: relative;
  animation: glowMusic 5s ease-in-out infinite alternate;
  z-index: 10;
}

@keyframes glowMusic {
  0% {
    text-shadow:
      0 0 40px #2db1ff,
      0 0 70px #ffdf6c,
      0 0 100px #ff6437;
    transform: scale(1);
  }
  100% {
    text-shadow:
      0 0 70px #20a0ea,
      0 0 90px #ffd632,
      0 0 130px #ff4500;
    transform: scale(1.05);
  }
}

.glass-subtitle {
  font-size: 1.4rem;
  font-weight: 300;
  color: rgba(180,210,255,0.75);
  text-shadow: 0 0 6px rgba(0,0,10,0.45);
  animation: subtitleFloat 6s ease-in-out infinite alternate;
  margin-bottom: 3rem;
}

@keyframes subtitleFloat {
  0%, 100% {opacity: 0.75; transform: translateY(-1px);}
  50% {opacity: 1; transform: translateY(2px);}
}

.chess-board-container {
  max-width: 580px;
  margin: 0 auto 3rem auto;
  padding: 1rem;
  background: rgba(20, 40, 80, 0.52);
  border-radius: 36px;
  box-shadow:
    inset 0 0 40px 0 rgba(50, 100, 220, 0.7),
    0 0 60px 5px rgba(255,215,20,0.45);
  border: 3px solid rgba(30, 60, 110, 0.6);
  display: flex;
  animation: boardPulse 20s ease-in-out infinite;
}

@keyframes boardPulse {
  0%, 100% {
    box-shadow:
      inset 0 0 30px 0 rgba(20,80,255,0.6),
      0 0 50px 10px rgba(220,180,30,0.45);
  }
  50% {
    box-shadow:
      inset 0 0 55px 5px rgba(64,160,255,0.85),
      0 0 120px 15px rgba(255,215,80,0.65);
  }
}

.chess-board-container img {
  border-radius: 28px !important;
  box-shadow:
    0 15px 70px rgba(0,0,50,0.7),
    0 0 50px 5px rgba(64,160,255,0.85);
  transition: all 0.6s ease;
  cursor: default;
  user-select: none;
}

.chess-board-container img:hover {
  transform: scale(1.04);
  box-shadow:
    0 20px 90px rgba(10,50,90,0.8),
    0 0 80px 10px rgba(255,215,30,0.7);
}

.chess-board-wrapper button {
  border-radius: 22px !important;
  border: 2.8px solid rgba(64, 158, 255, 0.45) !important;
  box-shadow:
    0 4px 16px 0 rgba(64, 160, 255, 0.7),
    inset 0 0 12px rgba(255, 255, 255, 0.13);
  font-family: 'SF Mono', monospace !important;
  font-weight: 800 !important;
  font-size: 2.8rem !important;
  color: #cdf0ff !important;
  background: linear-gradient(145deg, rgba(64, 158, 255, 0.12), rgba(80,180,255,0.28));
  height: 78px !important;
  width: 78px !important;
  margin: 2.5px !important;
  transition:
    background-color 0.3s ease,
    box-shadow 0.5s ease,
    transform 0.3s ease;
  box-sizing: border-box;
  user-select: none;
  position: relative;
  cursor: pointer;
}

.chess-board-wrapper button.dark {
  background: linear-gradient(145deg, rgba(12,18,38,0.55), rgba(8,13,29,0.78));
  color: #809fded3 !important;
  filter: drop-shadow(0 0 5px rgba(50,80,120,0.45));
  border: 2px solid rgba(20,40,80,0.6) !important;
}

.chess-board-wrapper button:hover {
  transform: scale(1.1);
  box-shadow:
    0 0 38px 4px rgba(64, 160, 255, 0.85),
    inset 0 0 14px rgba(255, 255, 255, 0.3);
  background: linear-gradient(145deg, rgba(70,180,255,0.5), rgba(80,210,255,0.75));
  color: #f0faff !important;
}

.chess-board-wrapper button.selected {
  background: #f2cb4e !important;
  box-shadow:
    0 0 52px 4px rgba(250, 215, 80, 0.95),
    inset 0 0 18px rgba(255, 255, 255, 0.55);
  color: #381e04 !important;
  cursor: pointer;
}

.chess-board-wrapper button.valid-move {
  background: rgba(64, 175, 255, 0.6) !important;
  color: #e0f4ff !important;
  box-shadow:
    0 0 35px 3px rgba(64, 175, 255, 0.7),
    inset 0 0 14px rgba(170, 220, 255, 0.5);
  cursor: pointer;
}

@keyframes pieceGlowPulse {
  0%, 100% { filter: drop-shadow(0 0 4px #69c5ff); }
  50% { filter: drop-shadow(0 0 11px #93d6ff); }
}

.piece-king {
  animation: pieceGlowPulse 3.6s ease-in-out infinite;
}
.piece-queen {
  animation: pieceGlowPulse 2.4s ease-in-out infinite;
}
.piece-rook {
  animation: pieceGlowPulse 4.4s ease-in-out infinite;
}
.piece-bishop {
  animation: pieceGlowPulse 3.8s ease-in-out infinite;
}
.piece-knight {
  animation: pieceGlowPulse 3.1s ease-in-out infinite;
}
.piece-pawn {
  animation: pieceGlowPulse 3.2s ease-in-out infinite;
}

.move-highlight {
  animation: moveGlow 6s ease-in-out infinite alternate;
}

@keyframes moveGlow {
  0%, 100% {
    box-shadow: 0 0 12px 6px rgba(255,215,72,0.7);
  }
  50% {
    box-shadow: 0 0 26px 14px rgba(255,215,72,1);
  }
}

.move-highlight-square {
  border-radius: 22px !important;
  box-shadow:
    0 0 18px 7px rgba(255,210,75,0.9);
}

/* Scrollbar for move history */
.move-history {
  background: rgba(255, 215, 50, 0.12);
  border-radius: 30px;
  padding: 18px 24px;
  box-shadow: 0 0 48px 12px rgba(255, 200, 80, 0.25);
  max-height: 500px;
  overflow-y: auto;
  font-weight: 600;
  color: #202020ef;
}

.move-history::-webkit-scrollbar {
  width: 12px;
}
.move-history::-webkit-scrollbar-track {
  background: transparent;
}
.move-history::-webkit-scrollbar-thumb {
  background: rgba(255, 225, 75, 0.8);
  border-radius: 10px;
}
.move-history::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 235, 120, 1);
}
