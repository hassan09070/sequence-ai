'use client';

import { Cell as CellType } from '@/types';

interface CellProps {
  cell: CellType;
  row: number;
  col: number;
  isLegalMove: boolean;
  onClick: () => void;
  isInSequence: boolean;
  sequencePlayerId: number | null;
}

export function Cell({
  cell,
  isLegalMove,
  onClick,
  isInSequence,
  sequencePlayerId,
}: CellProps) {
  const parseCard = (card: string) => {
    if (!card || card === 'WILD') {
      return { value: '', suit: '' };
    }
    const suit = card.slice(-1); // Last character is suit (H, D, C, S)
    const value = card.slice(0, -1); // Everything before is value
    return { value, suit };
  };

  const getSuitSymbol = (suit: string) => {
    const suits: Record<string, string> = {
      'H': '♥',
      'D': '♦',
      'C': '♣',
      'S': '♠'
    };
    return suits[suit] || '';
  };

  const getSuitColor = (suit: string) => {
    return (suit === 'H' || suit === 'D') ? 'text-red-600' : 'text-gray-900';
  };

  const { value, suit } = parseCard(cell.card);
  const isWild = cell.is_wild;
  const isOccupied = cell.chip !== null;

  // Chip colors for different players (Player 1 = blue, Player 2 = green)
  let chipColor = '';
  if (isOccupied) {
    if (cell.chip === 1) {
      chipColor = 'bg-blue-500 border-blue-700';
    } else if (cell.chip === 2) {
      chipColor = 'bg-green-500 border-green-700';
    }
  }

  // Sequence highlight (Player 1 = blue glow, Player 2 = green glow)
  let sequenceRing = '';
  if (isInSequence) {
    if (sequencePlayerId === 1) {
      sequenceRing = 'ring-4 ring-blue-400 shadow-[0_0_15px_rgba(59,130,246,0.6)]';
    } else if (sequencePlayerId === 2) {
      sequenceRing = 'ring-4 ring-green-400 shadow-[0_0_15px_rgba(34,197,94,0.6)]';
    }
  }

  // Wild/Corner cards
  if (isWild) {
    return (
      <div className="aspect-square bg-gradient-to-br from-purple-600 to-purple-800 rounded-lg shadow-lg flex items-center justify-center border-2 border-purple-500">
        <span className="text-3xl text-yellow-300">★</span>
      </div>
    );
  }

  return (
    <button
      onClick={onClick}
      disabled={!isLegalMove}
      className={`
        aspect-square relative rounded-lg shadow-lg transition-all duration-200
        ${isLegalMove ? 'cursor-pointer hover:scale-105 hover:shadow-xl' : 'cursor-not-allowed'}
        ${sequenceRing}
      `}
    >
      {/* Card Background */}
      <div
        className={`
          absolute inset-0 rounded-lg border-2
          ${isOccupied ? 'bg-gray-100 border-gray-400' : 'bg-white border-gray-300'}
          ${isLegalMove && !isOccupied ? 'ring-2 ring-yellow-400' : ''}
        `}
      >
        {/* Card Content */}
        <div className="absolute inset-0 flex flex-col items-center justify-center p-1">
          {/* Card Value */}
          <div className={`text-lg font-bold leading-none ${getSuitColor(suit)}`}>
            {value}
          </div>
          {/* Suit Symbol */}
          <div className={`text-2xl leading-none ${getSuitColor(suit)}`}>
            {getSuitSymbol(suit)}
          </div>
        </div>

        {/* Chip Overlay */}
        {isOccupied && (
          <div className="absolute inset-0 flex items-center justify-center bg-black/10 rounded-lg">
            <div
              className={`
                w-10 h-10 rounded-full ${chipColor}
                border-4 shadow-lg flex items-center justify-center
              `}
            >
              <div className="w-6 h-6 rounded-full border-2 border-white/30" />
            </div>
          </div>
        )}
      </div>
    </button>
  );
}
