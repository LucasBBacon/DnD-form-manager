import type { ActiveEffect, Trait } from "../types/types";

export const aggregateActiveEffects = (
  traitIds: string[],
  characterLevel: number,
  traitDatabase: Record<string, Trait>,
): ActiveEffect[] => {
  const activeEffects: ActiveEffect[] = [];

  traitIds.forEach((traitId) => {
    const trait = traitDatabase[traitId];

    if (!trait || !trait.effects) {
      console.warn(
        `Trait ID '${traitId}' not found in database or has no effects.`,
      );
      return;
    }

    trait.effects.forEach((effect) => {
      const requiredLevel = effect.level_available ?? 1;

      if (characterLevel >= requiredLevel) {
        activeEffects.push({
          ...effect,
          source_trait_id: trait.id,
          source_trait_name: trait.name,
        });
      }
    });
  });

  return activeEffects;
};
