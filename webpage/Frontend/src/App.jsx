import { useState } from 'react'
import './App.css'
import Card from './components/Card/Card'

// function getSpells() {
  // return ()
// }

function App() {
  const spells = fetch("http://localhost:3000/").then(res => res.json()).then(json => console.log(json))
  return (
    <>
      hello world
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
