import { create } from "zustand";
import raceDB from "../data/raceDB";
import type {
  AbilityScore,
  ActiveEffect,
  FinalStats,
  MergedRaceData,
  StatsRecord,
} from "../types/types";
import { mergeRaceAndSubrace } from "../utils/raceUtils";
import { aggregateActiveEffects } from "../utils/traitUtils";
import { calculateStats } from "../utils/statUtils";
import subraceDB from "../data/subraceDB";
import traitDB from "../data/traitDB";

interface CharacterState {
  characterLevel: number;
  baseStats: StatsRecord;
  selectedRaceId: string | null;
  selectedSubraceId: string | null;

  abilityScoreChoices: Partial<StatsRecord>;
  languageChoices: string[];
  traitChoices: Record<string, string[]>;

  setRace: (raceId: string) => void;
  setSubrace: (subraceId: string) => void;
  setAbilityScoreChoice: (stat: AbilityScore, value: number) => void;

  getMergedRace: () => MergedRaceData | null;
  getActiveEffects: () => ActiveEffect[];
  getFinalStats: () => FinalStats;
}

export const useCharacterStore = create<CharacterState>()((set, get) => ({
  characterLevel: 1,
  baseStats: { str: 10, dex: 10, con: 10, int: 10, wis: 10, cha: 10 },
  selectedRaceId: null,
  selectedSubraceId: null,

  abilityScoreChoices: {},
  languageChoices: [],
  traitChoices: {},

  setRace: (raceId) =>
    set((state) => {
      if (state.selectedRaceId === raceId) return state;

      return {
        selectedRaceId: raceId,
        selectedSubraceId: null,
        abilityScoreChoices: {},
        languageChoices: [],
        traitChoices: {},
      };
    }),

  setSubrace: (subraceId) =>
    set((state) => {
      if (state.selectedSubraceId === subraceId) return state;

      return {
        selectedSubraceId: subraceId,
        agilityScoreChoices: {},
        languageChoices: [],
        traitChoices: {},
      };
    }),

  setAbilityScoreChoice: (stat, value) =>
    set((state) => ({
      abilityScoreChoices: {
        ...state.abilityScoreChoices,
        [stat]: value,
      },
    })),

  getMergedRace: () => {
    const { selectedRaceId, selectedSubraceId } = get();
    if (!selectedRaceId) return null;

    const baseRace = raceDB[selectedRaceId];
    const subrace = selectedSubraceId
      ? subraceDB[selectedSubraceId]
      : undefined;

    return mergeRaceAndSubrace(baseRace, subrace);
  },

  getActiveEffects: () => {
    const mergedRace = get().getMergedRace();
    if (!mergedRace) return [];

    return aggregateActiveEffects(
      mergedRace.traits,
      get().characterLevel,
      traitDB,
    );
  },

  getFinalStats: () => {
    const mergedRace = get().getMergedRace();
    if (!mergedRace) {
      return calculateStats(get().baseStats, {} as MergedRaceData);
    }

    return calculateStats(
      get().baseStats,
      mergedRace,
      get().abilityScoreChoices,
      get().getActiveEffects(),
    );
  },
}));
