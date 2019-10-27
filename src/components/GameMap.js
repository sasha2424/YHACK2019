import React, { useState, useEffect } from 'react';
import GameTile from './GameTile';

function GameMap(props) {
  const [hovering, setHovering] = useState(null);
  const [position, setPosition] = useState([5, 0]);
  const [gradient, setGradient] = useState([...Array(100)].fill(0));
  const [state, setState] = useState([...Array(100)]);

  useEffect(() => {
    let interval = null;
    const setup = async () => {
      await fetch('http://localhost:5000/api/start', { method: 'POST', mode: 'no-cors' });

      interval = setInterval(() => {
        fetch('http://localhost:5000/api/step-visual', {
          method: 'POST',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Credentials': true,
          'Access-Control-Allow-Methods': 'POST',
          'Access-Control-Allow-Headers': 'Content-Type',
        }).then(response => response.json())
          .then(({ board, agent, qtable }) => { setState(board); setPosition(agent); setGradient(qtable); })
          .catch(() => clearInterval(interval));
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
          color={gradient[i]}
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
