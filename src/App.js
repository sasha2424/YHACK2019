import React from 'react';
import GameContainer from './components/GameContainer';
import LearningRateGraph from './components/LearningRateGraph';
import QTable from './components/QTable';
import ParameterControl from './components/ParameterControl';
import './App.css';

function App() {
  return (
    <div className="App">
      <GameContainer />
      <LearningRateGraph />
      <QTable />
      <ParameterControl />
    </div>
  );
}

export default App;
