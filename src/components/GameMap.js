import React, { useState } from 'react';
import GameTile from './GameTile';

function GameMap(props) {
  const [hovering, setHovering] = useState(null);
  const [position, setPosition] = useState(0);
  const [state, setState] = useState(new Array(100));

  return (
    <div className="GameMap" state= {{ stateArray: state }}>
      {[...Array(100)].map((_, i) =>
        <GameTile
          key={i}
          isPlayer={i === position}
          isHovering={hovering === i}
          onMouseOver={() => setHovering(i)}
          toPlace={props.selected}
          updateState={setState}
          state={state}
          index={i}
        />
      )}
      {console.log(state)}
    </div>
  );
}

export default GameMap;
