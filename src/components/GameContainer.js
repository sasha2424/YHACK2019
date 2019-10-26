import React from 'react';
import GameObjectSelector from './GameObjectSelector';
import GameMap from './GameMap';

function GameContainer(props) {
  return (
    <div className="GameContainer">
      <GameObjectSelector />
      <GameMap />
    </div>
  );
}

export default GameContainer;
