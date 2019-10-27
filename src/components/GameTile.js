import React from 'react';
import Sprite from './Sprite';
import chroma from 'chroma-js';

const f = chroma.scale(['008ae5', 'yellow']);
console.log(f(0.5).hex());

function GameTile(props) {
  return (
    <div
      className="GameTile"
      onMouseOver={props.onMouseOver}
      style={{ backgroundColor: props.isHovering ? 'green' : f(props.color).hex() }}
      onClick={props.updateState}
    >
      {props.icon && <Sprite icon={props.icon} />}
      {props.isPlayer && <Sprite icon="player" />}
    </div>
  );
}

export default GameTile;
