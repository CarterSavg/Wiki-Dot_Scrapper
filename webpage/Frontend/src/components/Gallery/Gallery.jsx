import { useState } from 'react'
import Card from '../Card/Card'

function Gallery({ spells }) {
    return (
        spells.map(spell =>
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
        )
    )
}

export default Gallery;
