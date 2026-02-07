import { useState } from 'react'
import './App.css'

// function getSpells() {
  // return ()
// }

function App() {
  const getSpells = fetch("http://localhost:3000/").then(res => res.json()).then(json => console.log(json))
  return (
    <>
      hello world
    </>
  )
}

export default App
