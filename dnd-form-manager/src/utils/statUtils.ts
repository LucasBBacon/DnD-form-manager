import type {
  AbilityScore,
  ActiveEffect,
  FinalStats,
  MergedRaceData,
  StatsRecord,
} from "../types/types";

export const calculateModifier = (score: number): number => {
  return Math.floor((score - 10) / 2);
};

const ABILITY_SCORES: AbilityScore[] = [
  "str",
  "dex",
  "con",
  "int",
  "wis",
  "cha",
];

export const calculateStats = (
  baseStats: StatsRecord,
  raceData: MergedRaceData,
  userChoices: Partial<StatsRecord> = {},
  activeEffects: ActiveEffect[] = [],
): FinalStats => {
  const finalStats = {} as FinalStats;

  ABILITY_SCORES.forEach((stat) => {
    let totalScore = baseStats[stat];

    // Add fixed racial bonuses
    if (raceData.ability_bonuses?.fixed?.[stat]) {
      totalScore += raceData.ability_bonuses.fixed[stat];
    }

    // Add user-selected racial choice bonuses
    if (userChoices[stat]) {
      totalScore += userChoices[stat] as number;
    }

    // Add active trait modifiers
    const traitModifiers = activeEffects.filter(
      (effect) => effect.type === "stat_modifier" && effect.target === stat,
    );

    traitModifiers.forEach((effect) => {
      if (typeof effect.value === "number") {
        totalScore += effect.value;
      }
    });

    // Assign the final score and calculated modifier
    finalStats[stat] = {
      score: totalScore,
      modifier: calculateModifier(totalScore),
    };
  });

  return finalStats;
};
