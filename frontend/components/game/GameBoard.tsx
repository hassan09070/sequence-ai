'use client';

import { Cell as CellType } from '@/types';
import { Cell } from './Cell';

interface GameBoardProps {
  board: CellType[][];
  legalMoves: Set<string>;
  onCellClick: (row: number, col: number) => void;
}

export function GameBoard({ board, legalMoves, onCellClick }: GameBoardProps) {
  const isLegalMove = (row: number, col: number): boolean => {
    return legalMoves.has(`${row},${col}`);
  };

  return (
    <div className="bg-gradient-to-br from-green-700 to-green-900 p-4 rounded-lg shadow-2xl">
      <div className="grid grid-cols-10 gap-1 max-w-3xl mx-auto">
        {board.map((row, rowIndex) =>
          row.map((cell, colIndex) => (
            <Cell
              key={`${rowIndex}-${colIndex}`}
              cell={cell}
              row={rowIndex}
              col={colIndex}
              isLegalMove={isLegalMove(rowIndex, colIndex)}
              onClick={() => onCellClick(rowIndex, colIndex)}
            />
          ))
        )}
      </div>
    </div>
  );
}
