def display_board(board):
    selected_square = st.session_state.get('selected_square', None)
    valid_moves = st.session_state.get('valid_moves', [])

    st.markdown('<div class="chess-board-container">', unsafe_allow_html=True)

    # Loop ranks 8->1 (7->0) and files a->h (0->7)
    for rank in range(7, -1, -1):
        cols = st.columns(8)
        for file in range(8):
            square = chess.square(file, rank)  # file + rank to square index
            piece = board.piece_at(square)

            # Maintain your piece symbols as is
            piece_symbols = {
                'k': '♔', 'q': '♕', 'r': '♖', 'b': '♗', 'n': '♘', 'p': '♙',
                'K': '♚', 'Q': '♛', 'R': '♜', 'B': '♝', 'N': '♞', 'P': '♟'
            }

            piece_symbol = piece_symbols.get(piece.symbol(), '') if piece else ''
            piece_class = ""
            if piece:
                pt = piece.symbol().lower()
                if pt == 'k':
                    piece_class = "piece-king"
                elif pt == 'q':
                    piece_class = "piece-queen"
                elif pt == 'r':
                    piece_class = "piece-rook"
                elif pt == 'b':
                    piece_class = "piece-bishop"
                elif pt == 'n':
                    piece_class = "piece-knight"
                elif pt == 'p':
                    piece_class = "piece-pawn"

            # Background color logic for squares
            bg_color = (
                'rgba(64, 156, 255, 0.8)' if square == selected_square
                else 'rgba(40, 167, 69, 0.8)' if any(move.to_square == square for move in valid_moves)
                else 'rgba(248, 249, 250, 0.9)' if (rank + file) % 2 == 0
                else 'rgba(108, 117, 125, 0.9)'
            )
            text_color = (
                'white' if square == selected_square or any(move.to_square == square for move in valid_moves) or ((rank + file) % 2 != 0)
                else 'black'
            )

            with cols[file]:
                tutor_hint = ""
                # If tutor mode and showing hints for selected square
                if st.session_state.get('tutor_mode', False) and st.session_state.get('show_hints', True):
                    hint_result = get_tutor_hint(board, selected_square)
                    if hint_result and selected_square == square:
                        hint_text, quality = hint_result
                        tutor_hint = f'<div class="tutor-hint">{hint_text}</div>'

                button_html = f'''
                <div style="position: relative;">
                    <button 
                        class="chess-square-button {piece_class}" 
                        onclick="handleChessClick({square})"
                        style="
                            background: {bg_color};
                            color: {text_color};
                            width: 100%;
                            height: 70px;
                            border-radius: 12px;
                            font-family: 'SF Mono', 'Monaco', 'Menlo', monospace;
                            font-weight: 700;
                            font-size: 2.5rem;
                            cursor: pointer;
                            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            position: relative;
                            overflow: hidden;
                        "
                        title="Square {chr(97 + file)}{rank + 1}">
                        {piece_symbol}
                    </button>
                    {tutor_hint}
                </div>
                '''
                st.markdown(button_html, unsafe_allow_html=True)

    # Inject JS for handling clicks without reloading page
    st.markdown("""
    <script>
    function handleChessClick(square) {
        // Remove any previous hidden input
        const prev = document.getElementById('chess-click-input');
        if(prev) prev.remove();
        // Create hidden input with the clicked square value
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'chess_square_click';
        input.value = square;
        input.id = 'chess-click-input';
        document.body.appendChild(input);
        // Dispatch a custom event Streamlit can intercept
        const event = new CustomEvent('chessSquareClick', { detail: { square: square } });
        document.dispatchEvent(event);
    }
    </script>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
