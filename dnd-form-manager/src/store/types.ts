export interface Speed {
    walk: number;
    fly?: number;
    swim?: number;
    climb?: number;
}

export interface Race {
    id: string;
    name: string;
    size: 'tiny' | 'small' | 'medium' | 'large';
    speed: Speed;
    ability_bonuses: {
        fixed?: Record<string, number>;
        choices?: { count: number; bonus: number; options: string[] };
    };
    traits: string[];
    languages: { known: string[]; choices?: number };
}

export interface Subrace {
    id: string;
    name: string;
    parent_race_id: string;
    ability_bonuses_additions: Record<string, number>;
    traits_added: string[];
    languages_added?: string[]
    overrides?: {
        speed?: Speed;
        size?: 'tiny' | 'small' | 'medium' | 'large';
    };
}

export interface MergedRaceData extends Race {
    subrace_name?: string;
}