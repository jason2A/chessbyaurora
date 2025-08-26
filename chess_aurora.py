import streamlit as st
import chess
import streamlit.components.v1 as components

if "board" not in st.session_state:
    st.session_state.board = chess.Board()

fen = st.session_state.board.fen()

html_code = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />

  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/chessboard.js/1.0.0/css/chessboard.min.css" />
  <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/chessboard.js/1.0.0/js/chessboard.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/chess.js/0.10.2/chess.min.js"></script>

  <style>
    :root {{
      --bg1: #0f0c29;
      --bg2: #302b63;
      --bg3: #24243e;
      --glass: rgba(255,255,255,0.08);
      --neon: rgba(0, 255, 255, 0.7);
      --cyan: #00e5ff;
      --magenta: #ff00c8;
      --lime: #73ff00;
      --text: #e9f1ff;
      --sub: #a8b3cf;
    }}

    * {{ box-sizing: border-box; }}
    html, body {{
      margin: 0;
      min-height: 100vh;
      color: var(--text);
      font-family: 'Segoe UI', system-ui, -apple-system, Roboto, Arial, sans-serif;
      background: radial-gradient(1200px 800px at 10% 10%, rgba(0,255,255,0.06), transparent 40%),
                  radial-gradient(1000px 700px at 90% 20%, rgba(255,0,200,0.05), transparent 45%),
                  linear-gradient(135deg, var(--bg1), var(--bg2), var(--bg3));
    }}

    .app {{
      width: 100%;
      display: flex;
      justify-content: center;
      padding: 32px 16px;
    }}

    .shell {{
      width: 100%;
      max-width: 1100px;
      display: grid;
      grid-template-columns: 1fr 340px;
      gap: 22px;
    }}

    @media (max-width: 980px) {{
      .shell {{ grid-template-columns: 1fr; }}
    }}

    .panel {{
      background: linear-gradient(180deg, rgba(255,255,255,0.10), rgba(255,255,255,0.06));
      backdrop-filter: blur(14px);
      border-radius: 20px;
      box-shadow:
        0 0 40px rgba(0, 255, 255, 0.25),
        inset 0 0 30px rgba(0, 180, 255, 0.15),
        0 10px 30px rgba(0,0,0,0.25);
      border: 1px solid rgba(255,255,255,0.12);
      overflow: hidden;
    }}

    .header {{
      padding: 16px 18px;
      border-bottom: 1px solid rgba(255,255,255,0.12);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .title {{
      font-weight: 700;
      letter-spacing: 0.4px;
    }}
    .sub {{ color: var(--sub); font-size: 12px; }}

    .board-wrap {{
      padding: 16px;
    }}

    #board {{
      width: 100%;
      max-width: 640px;
      margin: 0 auto;
      border-radius: 18px;
      padding: 10px;
      background: var(--glass);
      box-shadow:
        0 0 24px rgba(0, 255, 255, 0.35),
        inset 0 0 22px rgba(0, 180, 255, 0.22);
    }}

    /* chessboard.js squares and pieces */
    .square-55d63 {{ border-radius: 6px; transition: background 0.25s ease; }}
    .highlight-move {{ box-shadow: inset 0 0 18px var(--cyan), 0 0 18px var(--cyan) !important; border-radius: 8px; }}
    .highlight-legal {{ box-shadow: inset 0 0 10px rgba(0,255,255,0.7) !important; }}
    .piece-417db {{ filter: drop-shadow(0 0 8px var(--cyan)); transition: transform 0.2s ease, filter 0.25s ease; }}
    .piece-417db:hover {{ transform: translateY(-2px) scale(1.05); filter: drop-shadow(0 0 18px var(--magenta)); }}
    .piece-417db:active {{ transform: scale(1.08); filter: drop-shadow(0 0 22px var(--lime)); }}

    .controls {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0,1fr));
      gap: 10px;
      padding: 14px;
      background: rgba(0,0,0,0.20);
      border-top: 1px solid rgba(255,255,255,0.10);
    }}
    .btn {{
      padding: 10px 12px;
      border-radius: 12px;
      border: 1px solid rgba(255,255,255,0.14);
      background: linear-gradient(180deg, rgba(255,255,255,0.12), rgba(255,255,255,0.06));
      color: var(--text);
      cursor: pointer;
      font-weight: 600;
      letter-spacing: .2px;
      transition: transform .08s ease, box-shadow .18s ease, background .2s ease;
      text-align: center;
      user-select: none;
    }}
    .btn:hover {{ box-shadow: 0 8px 24px rgba(0,255,255,.25); }}
    .btn:active {{ transform: translateY(1px); }}

    .side {{
      display: flex;
      flex-direction: column;
      height: 100%;
    }}
    .section {{ padding: 14px 16px; border-bottom: 1px solid rgba(255,255,255,0.10); }}
    .label {{ color: var(--sub); font-size: 12px; margin-bottom: 6px; }}
    .value {{ font-weight: 700; }}

    .scroll {{
      max-height: 320px;
      overflow: auto;
      padding: 12px 16px;
    }}
    .scroll pre {{
      white-space: pre-wrap;
      word-wrap: break-word;
      margin: 0;
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace;
    }}

    .status {{
      padding: 14px 16px;
      background: rgba(0,0,0,0.20);
      border-top: 1px solid rgba(255,255,255,0.10);
      font-weight: 600;
    }}
  </style>
</head>
<body>
  <div class="app">
    <div class="shell">
      <div class="panel">
        <div class="header">
          <div>
            <div class="title">Aurora Chess</div>
            <div class="sub">Interactive board with neon glass UI</div>
          </div>
          <div class="sub" id="turnLabel">Turn: White</div>
        </div>

        <div class="board-wrap">
          <div id="board"></div>
        </div>

        <div class="controls">
          <div class="btn" id="btnReset">Reset</div>
          <div class="btn" id="btnUndo">Undo</div>
          <div class="btn" id="btnFlip">Flip</div>
        </div>
      </div>

      <div class="panel side">
        <div class="section">
          <div class="label">Orientation</div>
          <div class="value" id="orientationVal">white</div>
        </div>
        <div class="section">
          <div class="label">FEN</div>
          <div class="value" id="fenVal">{fen}</div>
        </div>
        <div class="section">
          <div class="label">PGN</div>
        </div>
        <div class="scroll">
          <pre id="pgnVal">(no moves yet)</pre>
        </div>
        <div class="status" id="statusVal">Game on. White to move.</div>
      </div>
    </div>
  </div>

  <audio id="sndMove" preload="auto" src="https://raw.githubusercontent.com/ornicar/lila/master/public/sound/standard/Move.mp3"></audio>
  <audio id="sndCapture" preload="auto" src="https://raw.githubusercontent.com/ornicar/lila/master/public/sound/standard/Capture.mp3"></audio>

  <script>
    var game = new Chess('{fen}');
    var currentOrientation = 'white';
    var lastSource = null, lastTarget = null;

    var board = Chessboard('board', {{
      draggable: true,
      position: '{fen}',
      pieceTheme: 'https://chessboardjs.com/img/chesspieces/wikipedia/{{{{piece}}}}.png',
      showNotation: true,
      onDragStart: onDragStart,
      onDrop: onDrop,
      onSnapEnd: onSnapEnd
    }});

    $(window).on('resize', function() {{
      board.resize();
    }});

    function playSound(move) {{
      var isCapture = !!(move && (move.flags && move.flags.indexOf('c') !== -1));
      document.getElementById(isCapture ? 'sndCapture' : 'sndMove').play().catch(function(){{}});
    }}

    function setStatus() {{
      var status = '';
      var moveColor = game.turn() === 'w' ? 'White' : 'Black';

      if (game.in_checkmate()) {{
        status = 'Checkmate. ' + (moveColor === 'White' ? 'Black' : 'White') + ' wins.';
      }} else if (game.in_draw()) {{
        status = 'Draw.';
      }} else {{
        status = 'Game on. ' + moveColor + ' to move' + (game.in_check() ? ' (in check)' : '') + '.';
      }}

      $('#turnLabel').text('Turn: ' + (game.turn() === 'w' ? 'White' : 'Black'));
      $('#statusVal').text(status);
      $('#fenVal').text(game.fen());
      var pgn = game.pgn();
      $('#pgnVal').text(pgn && pgn.length ? pgn : '(no moves yet)');
    }}

    function clearHighlights() {{
      $('.square-55d63').removeClass('highlight-move highlight-legal');
    }}

    function highlightMove(source, target) {{
      clearHighlights();
      if (source) $('.square-' + source).addClass('highlight-move');
      if (target) $('.square-' + target).addClass('highlight-move');
    }}

    function highlightLegal(from) {{
      clearHighlights();
      var moves = game.moves({{ square: from, verbose: true }});
      moves.forEach(function(m) {{
        $('.square-' + m.to).addClass('highlight-legal');
      }});
    }}

    function onDragStart(source, piece) {{
      if (game.game_over()) return false;
      if ((game.turn() === 'w' && piece.search(/^b/) !== -1) ||
          (game.turn() === 'b' && piece.search(/^w/) !== -1)) return false;
      highlightLegal(source);
    }}

    function onDrop(source, target) {{
      var move = game.move({{ from: source, to: target, promotion: 'q' }});
      clearHighlights();

      if (move === null) return 'snapback';

      lastSource = source;
      lastTarget = target;
      highlightMove(source, target);
      playSound(move);
      setStatus();
    }}

    function onSnapEnd() {{
      board.position(game.fen());
    }}

    // Controls
    $('#btnReset').on('click', function() {{
      game.reset();
      board.start();
      lastSource = lastTarget = null;
      clearHighlights();
      setStatus();
    }});

    $('#btnUndo').on('click', function() {{
      var undone = game.undo();
      if (undone) {{
        board.position(game.fen());
        lastSource = lastTarget = null;
        clearHighlights();
        setStatus();
      }}
    }});

    $('#btnFlip').on('click', function() {{
      board.flip();
      currentOrientation = currentOrientation === 'white' ? 'black' : 'white';
      $('#orientationVal').text(currentOrientation);
    }});

    // initial
    setStatus();
  </script>
</body>
</html>
"""

components.html(html_code, height=860, scrolling=True)
