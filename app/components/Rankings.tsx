import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { fetchLadder } from '../api/ladder';

function Ladder() {
  const { data: ladder, isLoading, error } = useQuery(['ladder'], fetchLadder);

  // ... loading and error handling ...

  return (
    <div>
      <h1>Ladder</h1>
      <ol>
        {ladder.map((player, index) => (
          <li key={player.id}>
            {player.name} (Rank: {index + 1})
          </li>
        ))}
      </ol>
    </div>
  );
}

export default Ladder;