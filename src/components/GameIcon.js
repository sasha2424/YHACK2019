import React from 'react';
import Sprite from './Sprite';

function GameIcon(props) {
  return (
    <div
      className="GameIcon"
      onClick={props.onClick}
      style={{ border: (props.isSelected) ? '1px solid green': '' }}
    >
      <Sprite icon={props.icon} />
    </div>
  );
}

export default GameIcon;
