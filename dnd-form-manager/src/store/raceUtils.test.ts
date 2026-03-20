import { describe, it, expect } from 'vitest'
import { mergeRaceAndSubrace } from './raceUtils'
import type { Race, Subrace } from './types'

describe('mergeRaceAndSubrace', () => {
    const mockDwarf: Race = {
        id: 'race_dwarf',
        name: 'Dwarf',
        size: 'medium',
        speed: { walk: 25 },
        ability_bonuses: { fixed: { con: 2 } },
        traits: ['trait_darkvision_60'],
        languages: { known: ['lang_common', 'lang_dwarvish'] }
    };

    const mockHillDwarf: Subrace = {
        id: 'subrace_dwarf_hill',
        name: 'Hill Dwarf',
        parent_race_id: 'race_dwarf',
        ability_bonuses_additions: { wis: 1 },
        traits_added: ['trait_dwarven_toughness']
    };

    const mockWoodElf: Subrace = {
            id: 'subrace_elf_wood',
            name: 'Wood Elf',
            parent_race_id: 'race_elf',
            ability_bonuses_additions: { wis: 1 },
            traits_added: ['trait_fleet_of_foot'],
            overrides: { speed: { walk: 35 } }
        };
        const mockElf: Race = { ...mockDwarf, id: 'race_elf', speed: { walk: 30} };

    it('should correctly merge a base race and subrace', () => {
        const result = mergeRaceAndSubrace(mockDwarf, mockHillDwarf);

        expect(result.name).toBe('Dwarf');
        expect(result.subrace_name).toBe('Hill Dwarf');
        expect(result.ability_bonuses.fixed?.con).toBe(2);
        expect(result.ability_bonuses.fixed?.wis).toBe(1);
        expect(result.traits).toContain('trait_darkvision_60');
        expect(result.traits).toContain('trait_dwarven_toughness');
    });

    it('should handle speed overrides if the subrace provides one', () => {
        const result = mergeRaceAndSubrace(mockElf, mockWoodElf);
        expect(result.speed.walk).toBe(35);
    });

    it('should throw an error if the subrace does not match the parent race', () => {
        expect(() => mergeRaceAndSubrace(mockDwarf, mockWoodElf)).toThrow();
    });
})