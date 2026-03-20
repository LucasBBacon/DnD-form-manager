import { describe, expect, it } from "vitest";
import type { Trait } from "./types";
import { aggregateActiveEffects } from "./traitUtils";

const mockTraitDB: Record<string, Trait> = {
    'trait_darkvision_60': {
        id: 'trait_darkvision_60',
        name: 'Darkvision',
        description: 'You can see in dim light within 60 feet...',
        effects: [
            { type: 'sense', target: 'darkvision', value: 60, level_available: 1 }
        ]
    },
    'trait_drow_magic': {
        id: 'trait_drow_magic',
        name: 'Drow Magic',
        description: 'You know the dancing lights cantrip. At 3rd level...',
        is_active: true,
        activation_type: 'action',
        effects: [
            { type: 'spell_grant', target: 'dancing_lights', spellcasting_ability: 'cha', level_available: 1 },
            { type: 'spell_grant', target: 'faerie_fire', spellcasting_ability: 'cha', level_available: 3 }
        ]
    },
    'trait_skill_versatility': {
        id: 'trait_skill_versatility',
        name: 'Skill Versatility',
        description: 'You gain proficiency in two skills of your choice.',
        effects: [
            { type: 'proficiency', choice: { count: 2, category: 'skill', pool: 'any_skill'}, level_available: 1 }
        ]
    }
};

describe('aggregateActiveEffects', () => {
    it('should aggregate base level 1 effects correctly', () => {
        const activeTraits = ['trait_darkvision_60', 'trait_skill_versatility'];
        const results = aggregateActiveEffects(activeTraits, 1, mockTraitDB);

        expect(results).toHaveLength(2);
        expect(results[0].target).toBe('darkvision');
        expect(results[1].choice?.count).toBe(2);
        expect(results[0].source_trait_name).toBe('Darkvision');
    });

    it('should filter out effects that are above the characters current level', () => {
        const activeTraits = ['trait_drow_magic'];
        const resultsLvl1 = aggregateActiveEffects(activeTraits, 1, mockTraitDB);

        expect(resultsLvl1).toHaveLength(1);
        expect(resultsLvl1[0].target).toBe('dancing_lights');

        const resultsLvl3 = aggregateActiveEffects(activeTraits, 3, mockTraitDB);

        expect(resultsLvl3).toHaveLength(2);
        expect(resultsLvl3[1].target).toBe('faerie_fire');
    });

    it('should default level_available to 1 if it is missing from the JSON', () => {
        const sloppyTraitDB: Record<string, Trait> = {
            'trait_sloppy': {
                id: 'trait_sloppy',
                name: 'Sloppy Trait',
                description: 'Missing level_available property',
                effects: [{type: 'resistance', target: 'fire'}]
            }
        };

        const results = aggregateActiveEffects(['trait_sloppy'], 1, sloppyTraitDB);
        expect(results).toHaveLength(1)
    });
    
    it( 'should ignore trait IDs that do not exist in the database,', () => {
        const results = aggregateActiveEffects(['trait_darkvision_60', 'trait_does_not_exist)'], 1, mockTraitDB);
        expect(results).toHaveLength(1)
    });
});