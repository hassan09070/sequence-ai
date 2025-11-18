'use client';

import { Player } from '@/types';
import { Card } from './Card';

interface PlayerHandProps {
  player: Player;
  selectedCard: string | null;
  onCardSelect: (card: string) => void;
  disabled?: boolean;
}

export function PlayerHand({ player, selectedCard, onCardSelect, disabled }: PlayerHandProps) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-4">
      <div className="mb-3">
        <h3 className="text-lg font-bold text-gray-800">{player.name}</h3>
        <p className="text-sm text-gray-600">
          Chips: {player.chips_remaining} | Cards: {player.hand.length}
        </p>
      </div>
      
      <div className="flex flex-wrap gap-2">
        {player.hand.map((card, index) => (
          <Card
            key={`${card}-${index}`}
            card={card}
            isSelected={selectedCard === card}
            onClick={() => onCardSelect(card)}
            disabled={disabled}
          />
        ))}
      </div>
    </div>
  );
}
