import { useState } from 'react'
import './Card.css'

function Card(props) {
    const [expanded, setExpanded] = useState(false)

    function toggleExpand() {
        setExpanded(!expanded)
    }

    return (
        <div onClick={toggleExpand}className="spell-card">
            <p className="spell-name"> {props.name}</p>
            <p className="casting-time">Casting Time: {props.castingTime} </p>
            <p className="spell-distance">Distance: {props.distance} </p>
            <p className="spell-school"> {props.school} </p>
            <p className="spell-level"> {props.level === 0 ? "Cantrip" : "Level: " + props.level}</p>
            {expanded && <p className="spell-description">{props.description} </p>}
            {expanded && <p className="spell-higher"> {props.higherLevel} </p>}
            <ul className="spell-component">
                <li className="verbal-tag">{props.verbal ? "V" : ""}</li>
                <li className="somatic-tag">{props.somatic ? "S" : ""}</li>
                <li className="material-tag">{props.material ? "M" : ""}</li>
            </ul>
            {expanded && <p className="material-desc"> {props.material ? "Material: " + props.materialDesc : null}</p>}
            {expanded && <ul>
                {props.users.map((user, index) => (
                    <li key={index}>{user}</li>
                ))}

            </ul>}
        </div>
    )
}

export default Card
