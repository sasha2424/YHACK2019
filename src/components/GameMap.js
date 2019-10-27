import React, { useState, useEffect } from 'react';
import GameTile from './GameTile';

function GameMap(props) {
  const [hovering, setHovering] = useState(null);
  const [position, setPosition] = useState([5, 0]);
  const [state, setState] = useState([...Array(100)]);

  useEffect(() => {
    let interval = null;
    const setup = async () => {
      await fetch('http://localhost:5000/api/start', { method: 'POST', mode: 'no-cors' });
      //fetch('http://localhost:5000/api/reset-visual', { method: 'POST', mode: 'no-cors' });

      interval = setInterval(async () => {
        const response = await fetch('http://localhost:5000/api/step-visual', {
          method: 'POST',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Credentials': true,
          'Access-Control-Allow-Methods': 'POST',
          'Access-Control-Allow-Headers': 'Content-Type',
        });
        console.log(response);
        const { board, agent } = await response.json();
        setState(board);
        setPosition(agent);
      }, 200);
    };

    setup();

    return () => clearInterval(interval);
  }, []);

  const updateState = (index, newIcon) => {
    const newState = [...state];
    newState[index] = newIcon;
    setState(newState);
    fetch(`http://localhost:5000/api/set-state`, {
      method: 'POST',
      mode: 'no-cors',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ board: newState, agent: position }),
    });
  };

  return (
    <div className="GameMap">
      {state.map((icon, i) =>
        <GameTile
          key={i}
          icon={icon}
          isPlayer={i === 10 * position[0] + position[1]}
          isHovering={hovering === i}
          onMouseOver={() => setHovering(i)}
          updateState={() => updateState(i, props.selected)}
        />
      )}
    </div>
  );
}

export default GameMap;
