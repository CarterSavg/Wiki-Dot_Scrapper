import { useState } from 'react'
import './Card.css'

function Card(props) {
    return (
        <div class="spell-card">
            <p class="spell-name"> {props.name}</p>
            <p class="casting-time">Casting Time: {props.castingTime} </p>
            <p class="spell-distance">Distance: {props.distance} </p>
            <p class="spell-school"> {props.school} </p>
            <p class="spell-level"> {props.level === 0 ? "Cantrip" : "Level: " + props.level}</p>
            <p class="spell-description">{props.description} </p>
            <p class="spell-higher"> {props.higherLevel} </p>
            <p class="spell-component">
                {props.verbal ? "V" : ""}
                {props.somatic ? "S" : ""}
                {props.material ? "M" : ""}
            </p>
            <p class="material-desc"> {props.material ? "Material: " + props.materialDesc : null}</p>
            <ul>
                {props.users.map((user, index) => (
                    <li key={index}>{user}</li>
                ))}

            </ul>
        </div>
    )
}

export default Card
