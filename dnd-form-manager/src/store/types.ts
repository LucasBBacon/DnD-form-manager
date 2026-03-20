export interface Speed {
  walk: number;
  fly?: number;
  swim?: number;
  climb?: number;
}

export interface Race {
  id: string;
  name: string;
  size: "tiny" | "small" | "medium" | "large";
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
  languages_added?: string[];
  overrides?: {
    speed?: Speed;
    size?: "tiny" | "small" | "medium" | "large";
  };
}

export interface MergedRaceData extends Race {
  subrace_name?: string;
}

export interface TraitEffect {
  type:
    | "sense"
    | "proficiency"
    | "immunity"
    | "resistance"
    | "advantage"
    | "spell_grant"
    | "stat_modifier"
    | "speed"
    | "ac_calc";
  level_available?: number;
  target?: string;
  value?: number | string | boolean;
  condition?: string;
  spellcasting_ability?: "str" | "dex" | "con" | "int" | "wis" | "cha";
  choice?: {
    count: number;
    category: "skill" | "tool" | "weapon" | "spell" | "language" | "armor";
    pool: string;
  };
}

export interface Trait {
  id: string;
  name: string;
  description: string;
  is_active?: boolean;
  activation_type?: "action" | "bonus_action" | "reaction" | "special";
  uses?: { count: number | string; reset: string };
  effects: TraitEffect[];
}

export interface ActiveEffect extends TraitEffect {
  source_trait_id: string;
  source_trait_name: string;
}
