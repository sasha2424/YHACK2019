import React from 'react';
import GameIcon from './GameIcon.js';

function GameObjectSelector(props) {
  const icons = ['wall', 'block', 'bomb', 'tele', null];

  return (
    <div className="GameObjectSelector">
      {icons.map((icon, i) =>
        <GameIcon
          key={i}
          icon={icon}
          isSelected={icon === props.selected}
          onClick={e => {
            props.setSelected(icon);
          }}
        />
      )}
    </div>
  );
}

export default GameObjectSelector;
