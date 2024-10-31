// import logo from './logo.svg';
import { Albums } from './components/Albums';
import { AlbumsCreate } from './components/AlbumsCreate';
import './App.css';

import {BrowserRouter, Routes, Route} from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Albums/>} />
        <Route path="/albums" element={<Albums/>} />
        <Route path="/albums/create" element={<AlbumsCreate/>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
