import type { MergedRaceData, Race, Subrace } from "../types/types";

export const mergeRaceAndSubrace = (baseRace: Race, subrace?: Subrace): MergedRaceData => {
    if (!subrace) {
        return { ...baseRace };
    }

    if (subrace.parent_race_id !== baseRace.id) {
        throw new Error(`Subrace ${subrace.name} does not belong to Race ${baseRace.name}.`);
    }

    const merged: MergedRaceData = JSON.parse(JSON.stringify(baseRace));
    merged.subrace_name = subrace.name

    if (subrace.ability_bonuses_additions) {
        merged.ability_bonuses.fixed = {
            ...merged.ability_bonuses.fixed,
            ...subrace.ability_bonuses_additions
        };
    }

    merged.traits = [...merged.traits, ...subrace.traits_added];
    if (subrace.languages_added) {
        merged.languages.known = [...merged.languages.known, ...subrace.languages_added];
    }

    if (subrace.overrides) {
        if (subrace.overrides.speed) {
            merged.speed = { ...merged.speed, ...subrace.overrides.speed };
        }
        if (subrace.overrides.size) {
            merged.size = subrace.overrides.size;
        }
    }

    return merged;
};