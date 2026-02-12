import { useState } from 'react'
import './Card.css'

function Card(props) {
  return (
    <div class="spell-card">
                <p class="spell-name"> {props.name}</p>
                <p class="casting-time">Casting Time: {props.casting_time} </p>
                <p class="spell-distance">Distance: {props.distance} </p>
                <p class="spell-school"> {props.school} </p>
                <p class="spell-level"> {props.level === 0 ? "Cantrip" : "Level: " + props.level}</p>
                <p class="spell-description">{props.description} </p>
                <p class="spell-higher"> {props.higher_level} </p>
                <p class="spell-component">
                    {props.verbal ? "V" : ""}
                    {props.somatic ? "S" : ""}
                    {props.component ? "M" : ""}
                </p>
                <p class="material-desc"> {props.component ? "Material: " + props.material_desc : null}</p>
                <ul>
                    { props.users.map((user, index) => (
                        <li key={index}>{user}</li>
                    ))}
                        
                </ul>
            </div>
  )
}

export default Card
