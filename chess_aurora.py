/* Chess squares styling */
.chess-square-button {
    border-radius: 12px !important;
    border: 3px solid rgba(64, 156, 255, 0.3) !important;
    font-family: 'SF Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 2rem !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow:
        0 4px 16px rgba(64, 156, 255, 0.2),
        0 0 0 1px rgba(64, 156, 255, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    min-height: 70px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    background: linear-gradient(135deg,
        rgba(64, 156, 255, 0.1),
        rgba(100, 200, 255, 0.15),
        rgba(64, 156, 255, 0.1)) !important;
}

/* Hover effect */
.chess-square-button:hover {
    background: linear-gradient(135deg,
        rgba(64, 190, 255, 0.3),
        rgba(100, 220, 255, 0.35),
        rgba(64, 190, 255, 0.3)) !important;
    box-shadow:
        0 8px 32px rgba(64, 190, 255, 0.5),
        0 0 0 2px rgba(64, 190, 255, 0.4),
        inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
    border-color: rgba(64, 190, 255, 0.7) !important;
    transform: scale(1.05) translateY(-2px) !important;
}

/* Selected piece highlight */
.chess-square-button.selected {
    background: rgba(0, 120, 255, 0.85) !important;
    border-color: rgba(0, 100, 255, 0.95) !important;
    box-shadow:
        0 0 20px rgba(0, 120, 255, 1),
        inset 0 1px 0 rgba(255, 255, 255, 0.4) !important;
    color: #d0eaff !important;
}

/* Valid moves highlight */
.chess-square-button.valid-move {
    background: rgba(0, 150, 255, 0.6) !important;
    border-color: rgba(0, 140, 255, 0.85) !important;
    box-shadow:
        0 0 15px rgba(0, 180, 255, 0.8),
        inset 0 1px 0 rgba(255, 255, 255, 0.25) !important;
    color: white !important;
}

/* Tutor hint styling */
.tutor-hint {
    position: absolute;
    top: -25px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(64, 156, 255, 0.95) !important;
    color: #000e2b !important;
    padding: 4px 8px;
    border-radius: 8px;
    font-size: 0.7rem;
    font-weight: 600;
    white-space: nowrap;
    z-index: 1000;
    animation: hintFloat 2s ease-in-out infinite;
    box-shadow: 0 0 25px rgba(64, 156, 255, 0.8) !important;
}
