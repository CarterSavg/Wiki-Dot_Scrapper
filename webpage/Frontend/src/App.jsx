import { useState, useEffect } from 'react'
import './App.css'
import Card from './components/Card/Card'
import Gallery from './components/Gallery/Gallery'
import LoadingIcon from './components/LoadingIcon/LoadingIcon'
import Filter from "./components/Filter/Filter";

function App() {
  const backendURL = import.meta.env.VITE_BACKEND_URL;
  const [spells, setSpells] = useState([])
  const [spellsLoading, setSpellsLoading] = useState(false)

  useEffect(() => {
    async function loadSpells() {
      setSpellsLoading(true)

      let response = await fetch(`http://${backendURL}`)
      let res = await response.json()

      setSpells(res)
      setSpellsLoading(false)
    }

    loadSpells();
  }, []);

  return (
    <>
      {spellsLoading && <LoadingIcon/>}
      {!spellsLoading && <Filter />}
      {!spellsLoading && <Gallery spells = {spells}/>}
    </>
  )
}

export default App
