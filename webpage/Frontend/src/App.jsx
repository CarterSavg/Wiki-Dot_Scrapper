import { useState, useEffect } from 'react'
import './App.css'
import Card from './components/Card/Card'

function App() {
  const [spells, setSpells] = useState([])
  const [spellsLoading, setSpellsLoading] = useState(false)

  useEffect(() => {
    async function loadSpells() {
      setSpellsLoading(true)

      let response = await fetch("http://localhost:3000/")
      let res = await response.json()

      setSpells(res)

      setSpellsLoading(false)
    }

    loadSpells();
  }, []);

spells.map(spell => console.log("new line " + spell.name))
  
  return (
    <>
      <Card
        key = {1}
        name = "Jump"
        castingTime = "1 Action"
        distance = "Self"
        school = "Abjuration"
        level = "1"
        description = "JUMP LEL"
        higherLevel = "Nothing"
        verbal = "V"
        somatic = ""
        material = "M"
        materialDesc = "I dont remeber"
        users = {["Wizard", "Warlock"]}
      />
    </>
  )
}

export default App
