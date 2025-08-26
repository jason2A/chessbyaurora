def display_board(board):
    selected_square = st.session_state.get('selected_square', None)
    valid_moves = st.session_state.get('valid_moves', [])

    st.markdown('<div class="chess-board-container">', unsafe_allow_html=True)
    
    # Iterate ranks 8 to 1 (7 to 0 zero-indexed)
    for rank in range(7, -1, -1):
        cols = st.columns(8)
        for file in range(8):
            square = chess.square(file, rank)  # standard indexing a1=0, h8=63
            
            piece = board.piece_at(square)
            piece_symbol = ""
            piece_class = ""
            if piece:
                piece_symbols = {
                    'k': '♔', 'q': '♕', 'r': '♖',
                    'b': '♗', 'n': '♘', 'p': '♙',
                    'K': '♚', 'Q': '♛', 'R': '♜',
                    'B': '♝', 'N': '♞', 'P': '♟'
                }
                piece_symbol = piece_symbols.get(piece.symbol(), piece.symbol())
                piece_type = piece.symbol().lower()
                # Add piece-specific animation class if needed
                if piece_type == 'k':
                    piece_class = "piece-king"
                elif piece_type == 'q':
                    piece_class = "piece-queen"
                elif piece_type == 'r':
                    piece_class = "piece-rook"
                elif piece_type == 'b':
                    piece_class = "piece-bishop"
                elif piece_type == 'n':
                    piece_class = "piece-knight"
                elif piece_type == 'p':
                    piece_class = "piece-pawn"

            with cols[file]:
                tutor_hint = ""
                # Check tutor hints if needed
                if st.session_state.get('tutor_mode', False) and st.session_state.get('show_hints', True):
                    hint_result = get_tutor_hint(board, selected_square)
                    if hint_result and selected_square == square:
                        hint_text, quality = hint_result
                        tutor_hint = f'<div class="tutor-hint">{hint_text}</div>'
                
                bg_color = 'rgba(64, 156, 255, 0.8)' if square == selected_square else \
                           'rgba(40, 167, 69, 0.8)' if any(move.to_square == square for move in valid_moves) else \
                           'rgba(248, 249, 250, 0.9)' if (rank + file) % 2 == 0 else 'rgba(108, 117, 125, 0.9)'
                text_color = 'white' if square == selected_square or any(move.to_square == square for move in valid_moves) or ((rank + file) % 2 != 0) else 'black'
                
                button_html = f'''
                <div style="position: relative;">
                <button class="chess-square-button {piece_class}" onclick="handleChessClick({square})"
                    style="
                        background: {bg_color};
                        color: {text_color};
                        width: 100%;
                        height: 70px;
                        border-radius: 12px;
                        font-family: 'SF Mono', 'Menlo', monospace;
                        font-weight: 700;
                        font-size: 2.5rem;
                        cursor: pointer;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        position: relative;
                        overflow: hidden;">
                    {piece_symbol}
                </button>
                {tutor_hint}
                </div>
                '''
                st.markdown(button_html, unsafe_allow_html=True)

    # JavaScript for clicks stays as in your code (unchanged)
    st.markdown("""
    <script>
    function handleChessClick(square) {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'chess_square_click';
        input.value = square;
        input.id = 'chess-click-input';
        const existing = document.getElementById('chess-click-input');
        if (existing) existing.remove();
        document.body.appendChild(input);
        const event = new CustomEvent('chessSquareClick', { detail: { square: square } });
        document.dispatchEvent(event);
    }
    </script>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
