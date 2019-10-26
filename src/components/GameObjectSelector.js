import React from 'react';
import GameIcon from './GameIcon.js';

function GameObjectSelector(props) {
  const icons = ['block', 'bomb', 'tele'];
  return (
    <div className="GameObjectSelector">
    {icons.map(x => <GameIcon id = {x} />)}
    </div>
  );
}

export default GameObjectSelector;
