'use client';

import { Cell as CellType } from '@/types';

interface CellProps {
  cell: CellType;
  row: number;
  col: number;
  isLegalMove: boolean;
  onClick: () => void;
  isInSequence?: boolean;
  sequencePlayerId?: number | null;
}

const getCardColor = (card: string): string => {
  if (!card || card === 'WILD') return '';
  const suit = card.slice(-1);
  return suit === 'H' || suit === 'D' ? 'text-red-600' : 'text-gray-800';
};

const getChipColor = (chip: number | null): string => {
  if (chip === 1) return 'bg-blue-500';
  if (chip === 2) return 'bg-green-500';
  if (chip === 3) return 'bg-yellow-500';
  return '';
};

const getSequenceGlow = (playerId: number | null): string => {
  if (playerId === 1) return 'ring-4 ring-blue-400 ring-opacity-75 shadow-[0_0_20px_rgba(59,130,246,0.8)]';
  if (playerId === 2) return 'ring-4 ring-green-400 ring-opacity-75 shadow-[0_0_20px_rgba(34,197,94,0.8)]';
  return '';
};

export function Cell({ cell, row, col, isLegalMove, onClick, isInSequence = false, sequencePlayerId = null }: CellProps) {
  const isWild = cell.is_wild;
  const hasChip = cell.chip !== null;
  const cardColor = getCardColor(cell.card);
  const chipColor = getChipColor(cell.chip);
  const sequenceGlow = isInSequence ? getSequenceGlow(sequencePlayerId) : '';

  return (
    <button
      onClick={onClick}
      disabled={!isLegalMove}
      className={`
        relative aspect-square border border-gray-300 rounded-sm
        flex items-center justify-center
        transition-all duration-200 overflow-hidden
        ${isWild ? 'bg-gradient-to-br from-purple-400 to-pink-400' : 'bg-white'}
        ${isLegalMove ? 'hover:bg-yellow-100 hover:scale-105 cursor-pointer ring-2 ring-yellow-400' : ''}
        ${hasChip ? 'cursor-not-allowed' : ''}
        ${!isLegalMove && !hasChip ? 'cursor-default' : ''}
        ${sequenceGlow}
      `}
      title={`${cell.card} at (${row}, ${col})${isInSequence ? ' - Part of sequence!' : ''}`}
    >
      {/* Card text */}
      <div className={`text-xs font-bold ${cardColor} ${hasChip ? 'opacity-30' : 'opacity-100'}`}>
        {isWild ? '★' : cell.card}
      </div>

      {/* Chip overlay */}
      {hasChip && (
        <div className={`absolute inset-1 rounded-full ${chipColor} shadow-lg flex items-center justify-center`}>
          <span className="text-white text-xs font-bold">{cell.chip}</span>
        </div>
      )}

      {/* Sequence indicator - small star in corner */}
      {isInSequence && (
        <div className="absolute top-0 right-0 bg-yellow-400 rounded-bl-lg px-1">
          <span className="text-xs">⭐</span>
        </div>
      )}

      {/* Legal move indicator */}
      {isLegalMove && !hasChip && (
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="w-2 h-2 bg-yellow-500 rounded-full animate-pulse" />
        </div>
      )}
    </button>
  );
}
