import React from 'react';
import Sprite from './Sprite';

function GameTile(props) {
  return (
    <div
      className="GameTile"
      onMouseOver={props.onMouseOver}
      style={{ backgroundColor: props.isHovering ? 'green' : '' }}
      onClick={props.updateState}
    >
      {props.icon && <Sprite icon={props.icon} />}
      {props.isPlayer && <Sprite icon="player" />}
    </div>
  );
}

export default GameTile;
