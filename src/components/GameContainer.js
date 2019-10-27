import React, { useState } from 'react';
import GameObjectSelector from './GameObjectSelector';
import GameMap from './GameMap';

function GameContainer(props) {
  const [selected, setSelected] = useState(null);
  
  return (
    <div className="GameContainer">
      <GameObjectSelector selected={selected} setSelected={setSelected}/>
      <GameMap selected={selected} />
    </div>
  );
}

export default GameContainer;
