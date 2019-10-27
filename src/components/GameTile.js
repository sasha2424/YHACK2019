import React, { useState } from 'react';
import Sprite from './Sprite';

function GameTile(props) {
    const [placed, setPlaced] = useState(null);
  return (
    <div
        className="GameTile"
        onMouseOver={props.onMouseOver}
        style={{ backgroundColor: props.isHovering?'green':'' }}
        onClick={() => {
            if(props.isHovering){
                setPlaced(props.toPlace);
                let newState = props.state;
                newState[props.index] = props.toPlace;
                props.updateState(newState)}}}
    >
        {placed && <Sprite icon={placed} />}
        {props.isPlayer && <Sprite icon="player" />}
    </div>
  )
}

export default GameTile;
