// AuroraChess.jsx
import React, { useMemo, useState } from "react";
import { Chess } from "chess.js";
import { Chessboard } from "react-chessboard";

export default function AuroraChess() {
  const [game] = useState(() => new Chess());
  const [fen, setFen] = useState(() => game.fen());
  const [orientation, setOrientation] = useState("white");
  const [pieceSet, setPieceSet] = useState("cburnett"); // cburnett | alpha | wikipedia

  const PIECE_SETS = {
    cburnett: "https://raw.githubusercontent.com/lichess-org/lila/master/public/piece/cburnett/{piece}.svg",
    alpha: "https://chessboardjs.com/img/chesspieces/alpha/{piece}.png",
    wikipedia: "https://chessboardjs.com/img/chesspieces/wikipedia/{piece}.png",
  };

  const makePieces = (base) => {
    const names = ["wP","wR","wN","wB","wQ","wK","bP","bR","bN","bB","bQ","bK"];
    const map = {};
    names.forEach((code) => {
      map[code] = ({ squareWidth }) => {
        const src = base.replace("{piece}", code);
        return (
          <img
            src={src}
            alt={code}
            style={{
              width: squareWidth,
              height: squareWidth,
              filter: "drop-shadow(0 0 8px rgba(0,255,255,0.5))",
            }}
            draggable={false}
          />
        );
      };
    });
    return map;
  };

  const customPieces = useMemo(() => makePieces(PIECE_SETS[pieceSet]), [pieceSet]);

  function onDrop(source, target) {
    const move = game.move({ from: source, to: target, promotion: "q" });
    if (!move) return false;
    setFen(game.fen());
    return true;
  }

  function reset() {
    game.reset();
    setFen(game.fen());
  }

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "grid",
        placeItems: "center",
        background:
          "radial-gradient(1200px 800px at 10% 10%, rgba(0,255,255,0.06), transparent 40%), radial-gradient(1000px 700px at 90% 20%, rgba(255,0,200,0.05), transparent 45%), linear-gradient(135deg, #0f0c29, #302b63, #24243e)",
        color: "#e9f1ff",
        fontFamily: "Segoe UI, system-ui, -apple-system, Roboto, Arial, sans-serif",
        padding: 20,
      }}
    >
      <div
        style={{
          display: "grid",
          gap: 16,
          gridTemplateColumns: "minmax(280px, 640px) 300px",
          alignItems: "start",
        }}
      >
        <div
          style={{
            background: "linear-gradient(180deg, rgba(255,255,255,0.10), rgba(255,255,255,0.06))",
            backdropFilter: "blur(14px)",
            borderRadius: 20,
            boxShadow:
              "0 0 40px rgba(0, 255, 255, 0.25), inset 0 0 30px rgba(0, 180, 255, 0.15), 0 10px 30px rgba(0,0,0,0.25)",
            border: "1px solid rgba(255,255,255,0.12)",
            padding: 16,
          }}
        >
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 12 }}>
            <div>
              <div style={{ fontWeight: 700 }}>Aurora Chess</div>
              <div style={{ fontSize: 12, color: "#a8b3cf" }}>
                {game.turn() === "w" ? "White" : "Black"} to move
              </div>
            </div>
            <div style={{ display: "flex", gap: 8 }}>
              <button onClick={reset} style={btnStyle}>Reset</button>
              <button
                onClick={() => {
                  const u = game.undo();
                  if (u) setFen(game.fen());
                }}
                style={btnStyle}
              >
                Undo
              </button>
              <button
                onClick={() => setOrientation((o) => (o === "white" ? "black" : "white"))}
                style={btnStyle}
              >
                Flip
              </button>
            </div>
          </div>

          <div
            style={{
              borderRadius: 18,
              padding: 10,
              background: "rgba(255,255,255,0.08)",
              boxShadow: "0 0 24px rgba(0, 255, 255, 0.35), inset 0 0 22px rgba(0, 180, 255, 0.22)",
            }}
          >
            <Chessboard
              position={fen}
              onPieceDrop={onDrop}
              boardOrientation={orientation}
              boardWidth={Math.min(640, Math.max(320, Math.floor(window.innerWidth * 0.8)))}
              customDarkSquareStyle={{ backgroundColor: "#2f345a", borderRadius: 6 }}
              customLightSquareStyle={{ backgroundColor: "#a6b1e1", borderRadius: 6 }}
              customBoardStyle={{ borderRadius: 12 }}
              customPieces={customPieces}
              animationDuration={200}
              showBoardNotation
            />
          </div>

          <div style={{ marginTop: 12, display: "flex", gap: 8, alignItems: "center" }}>
            <label style={{ fontSize: 12, color: "#a8b3cf" }}>Piece set</label>
            <select
              value={pieceSet}
              onChange={(e) => setPieceSet(e.target.value)}
              style={{
                ...btnStyle,
                padding: "8px 10px",
                cursor: "pointer",
              }}
            >
              <option value="cburnett">cBurnett (SVG, crisp)</option>
              <option value="alpha">Alpha (flat PNG)</option>
              <option value="wikipedia">Wikipedia (classic PNG)</option>
            </select>
          </div>
        </div>

        <div
          style={{
            background: "linear-gradient(180deg, rgba(255,255,255,0.10), rgba(255,255,255,0.06))",
            backdropFilter: "blur(14px)",
            borderRadius: 20,
            boxShadow:
              "0 0 40px rgba(0, 255, 255, 0.25), inset 0 0 30px rgba(0, 180, 255, 0.15), 0 10px 30px rgba(0,0,0,0.25)",
            border: "1px solid rgba(255,255,255,0.12)",
            padding: 16,
            minHeight: 200,
          }}
        >
          <div style={{ fontSize: 12, color: "#a8b3cf", marginBottom: 6 }}>FEN</div>
          <div style={{ fontWeight: 700, wordBreak: "break-word" }}>{fen}</div>
          <div style={{ height: 12 }} />
          <div style={{ fontSize: 12, color: "#a8b3cf", marginBottom: 6 }}>PGN</div>
          <div style={{ whiteSpace: "pre-wrap", wordBreak: "break-word" }}>
            {game.pgn() || "(no moves yet)"}
          </div>
        </div>
      </div>
    </div>
  );
}

const btnStyle = {
  padding: "8px 12px",
  borderRadius: 10,
  border: "1px solid rgba(255,255,255,0.14)",
  background: "linear-gradient(180deg, rgba(255,255,255,0.12), rgba(255,255,255,0.06))",
  color: "#e9f1ff",
  fontWeight: 600,
  letterSpacing: ".2px",
  cursor: "pointer",
};
