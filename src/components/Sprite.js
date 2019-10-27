import React from 'react';
import robot from '../assets/robot.svg';
import wall from '../assets/wall.svg';
import bomb from '../assets/bomb.svg';
import crate from '../assets/crate.svg';
import teleporter from '../assets/teleporter.svg';

const images = {
  player: robot,
  wall,
  bomb,
  block: crate,
  tele: teleporter,
};

function Sprite(props) {
    return <img className="Sprite" src={images[props.icon]} width="100%" height="100%" />;
}

export default Sprite;