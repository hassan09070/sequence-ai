'use client';

interface CardProps {
  card: string;
  isSelected: boolean;
  onClick: () => void;
  disabled?: boolean;
}

const getCardColor = (card: string): string => {
  if (!card) return '';
  const suit = card.slice(-1);
  if (suit === 'H' || suit === 'D') return 'text-red-600';
  return 'text-gray-800';
};

const getCardSuitSymbol = (card: string): string => {
  if (!card || card.length < 2) return '';
  const suit = card.slice(-1);
  switch (suit) {
    case 'H': return '♥';
    case 'D': return '♦';
    case 'C': return '♣';
    case 'S': return '♠';
    default: return '';
  }
};

const formatCardValue = (card: string): string => {
  if (!card || card.length < 2) return card;
  return card.slice(0, -1);
};

export function Card({ card, isSelected, onClick, disabled }: CardProps) {
  const color = getCardColor(card);
  const suit = getCardSuitSymbol(card);
  const value = formatCardValue(card);

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`
        relative bg-white rounded-lg shadow-lg p-3
        min-w-[60px] h-[90px]
        flex flex-col items-center justify-between
        transition-all duration-200
        ${isSelected ? 'ring-4 ring-blue-500 scale-105 -translate-y-2' : 'hover:scale-105'}
        ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover:shadow-xl'}
      `}
    >
      <div className={`text-xl font-bold ${color}`}>
        {value}
      </div>
      <div className={`text-3xl ${color}`}>
        {suit}
      </div>
      <div className={`text-xl font-bold ${color} opacity-50 rotate-180`}>
        {value}
      </div>
    </button>
  );
}
