import streamlit as st
import chess
import chess.svg
import base64
from io import BytesIO
import time
import random
import requests
import re
import os

# Page configuration
st.set_page_config(
    page_title="💎 Glass Chess",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Glassy ICE theme: only blue, violet, silver hues, no orange/gold/warm colors ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&family=SF+Mono:wght@400;500;600&display=swap');

    * { transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);}
    .main {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%);
        background-size: 400% 400%;
        animation: glassGradient 12s ease infinite;
        min-height: 100vh;
        padding: 0;
    }
    @keyframes glassGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%);
        background-size: 400% 400%;
        animation: glassGradient 12s ease infinite;
    }
    .glass-container {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border-radius: 32px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 3rem;
        margin: 2rem auto;
        max-width: 1400px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3),0 0 0 1px rgba(255, 255, 255, 0.05),inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
        animation: containerFloat 6s ease-in-out infinite;
    }
    @keyframes containerFloat {
        0%, 100% { transform: translateY(0px);}
        50% { transform: translateY(-8px);}
    }
    .glass-title {
        text-align: center;
        color: #ffffff;
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 700;
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 20px rgba(64, 156, 255, 0.5), 0 0 40px rgba(138, 43, 226, 0.3);
        animation: glassTitle 4s ease-in-out infinite alternate;
        letter-spacing: -0.02em;
        position: relative;
    }
    .glass-title::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 0;
        height: 2px;
        background: linear-gradient(90deg, #409cff, #533483);
        animation: titleUnderline 3s ease-in-out infinite;
    }
    @keyframes titleUnderline {
        0%, 100% { width: 0; opacity: 0;}
        50% { width: 200px; opacity: 1;}
    }
    @keyframes glassTitle {
        0% {
            text-shadow: 0 0 20px rgba(64, 156, 255, 0.5), 0 0 40px rgba(138, 43, 226, 0.3);
            transform: scale(1) rotateY(0deg);
        }
        100% {
            text-shadow: 0 0 30px rgba(138, 43, 226, 0.6), 0 0 50px rgba(64, 156, 255, 0.4);
            transform: scale(1.02) rotateY(2deg);
        }
    }
    .glass-subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.8);
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 400;
        font-size: 1.2rem;
        margin-bottom: 2.5rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        letter-spacing: 0.01em;
        animation: subtitleGlow 5s ease-in-out infinite;
    }
    .chess-board-container {
        display: flex;
        justify-content: center;
        margin: 2.5rem 0;
        position: relative;
        animation: boardContainerPulse
