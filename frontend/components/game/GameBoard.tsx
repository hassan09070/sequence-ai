'use client';

import { Cell as CellType } from '@/types';
import { Cell } from './Cell';

interface GameBoardProps {
  board: CellType[][];
  legalMoves: Set<string>;
  onCellClick: (row: number, col: number) => void;
  sequences?: Record<number, [number, number][][]>;
}

export function GameBoard({ board, legalMoves, onCellClick, sequences = {} }: GameBoardProps) {
  const isLegalMove = (row: number, col: number): boolean => {
    return legalMoves.has(`${row},${col}`);
  };

  const isInSequence = (row: number, col: number): { inSequence: boolean; playerId: number | null } => {
    for (const [playerIdStr, playerSequences] of Object.entries(sequences)) {
      const playerId = parseInt(playerIdStr);
      for (const sequence of playerSequences) {
        if (sequence.some(([r, c]) => r === row && c === col)) {
          return { inSequence: true, playerId };
        }
      }
    }
    return { inSequence: false, playerId: null };
  };

  return (
    <div className="bg-gradient-to-br from-green-700 to-green-900 p-4 rounded-lg shadow-2xl">
      <div className="grid grid-cols-10 gap-1 max-w-3xl mx-auto">
        {board.map((row, rowIndex) =>
          row.map((cell, colIndex) => {
            const sequenceInfo = isInSequence(rowIndex, colIndex);
            return (
              <Cell
                key={`${rowIndex}-${colIndex}`}
                cell={cell}
                row={rowIndex}
                col={colIndex}
                isLegalMove={isLegalMove(rowIndex, colIndex)}
                onClick={() => onCellClick(rowIndex, colIndex)}
                isInSequence={sequenceInfo.inSequence}
                sequencePlayerId={sequenceInfo.playerId}
              />
            );
          })
        )}
      </div>
    </div>
  );
}
