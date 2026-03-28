import { useState } from 'react'
import './Card.css'

function Card(props) {
    const [expanded, setExpanded] = useState(false)

    function toggleExpand() {
        setExpanded(!expanded)
    }

    return (
        <div onClick={toggleExpand}class="spell-card">
            <p class="spell-name"> {props.name}</p>
            <p class="casting-time">Casting Time: {props.castingTime} </p>
            <p class="spell-distance">Distance: {props.distance} </p>
            <p class="spell-school"> {props.school} </p>
            <p class="spell-level"> {props.level === 0 ? "Cantrip" : "Level: " + props.level}</p>
            {expanded && <p class="spell-description">{props.description} </p>}
            {expanded && <p class="spell-higher"> {props.higherLevel} </p>}
            <p class="spell-component">
                {props.verbal ? "V" : ""}
                {props.somatic ? "S" : ""}
                {props.material ? "M" : ""}
            </p>
            {expanded && <p class="material-desc"> {props.material ? "Material: " + props.materialDesc : null}</p>}
            {expanded && <ul>
                {props.users.map((user, index) => (
                    <li key={index}>{user}</li>
                ))}

            </ul>}
        </div>
    )
}

export default Card
