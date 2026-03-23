import { useState, useEffect } from 'react'
import './App.css'
import Card from './components/Card/Card'
import LoadingIcon from './components/LoadingIcon/LoadingIcon'

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


  return (
    <>
      {spellsLoading && <LoadingIcon/>}
      {!spellsLoading && spells.map(spell =>
        <Card
        key = {spell.id}
        name = {spell.name}
        castingTime = {spell.casting_time}
        distance = {spell.distance}
        school = {spell.school}
        level = {spell.level}
        description = {spell.description}
        higherLevel = {spell.higher_level}
        verbal = {spell.verbal}
        somatic = {spell.somatic}
        material = {spell.component}
        materialDesc = {spell.material_desc}
        users = {spell.users}
        />
      )}
    </>
  )
}

export default App
