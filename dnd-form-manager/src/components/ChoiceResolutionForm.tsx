import React from "react";
import { useCharacterStore } from "../store/characterStore";
import type { AbilityScore } from "../types/types";

export const ChoiceResolutionForm = () => {
  const mergedRace = useCharacterStore((state) => state.getMergedRace());
  const activeEffects = useCharacterStore((state) => state.getActiveEffects());

  const abilityChoices = useCharacterStore(
    (state) => state.abilityScoreChoices,
  );
  const setAbilityChoice = useCharacterStore(
    (state) => state.setAbilityScoreChoice,
  );

  if (!mergedRace) return null;

  const selectedAbilityCount = Object.keys(abilityChoices).length;

  const asiRules = mergedRace.ability_bonuses?.choices;
  const languageChoiceCount = mergedRace.languages?.choices || 0;

  const traitRequiringChoices = activeEffects.filter((effect) => effect.choice);

  return (
    <div>
      <h2>Pending Choices</h2>

      {/* --- SECTION A: Ability Score Choices --- */}
      {asiRules && (
        <div>
          <h3>Ability Score Increase (Choose {asiRules.count})</h3>
          <p>Each grants a +{asiRules.bonus} bonus.</p>

          <div>
            {asiRules.options.map((stat) => {
              const isSelected = !!abilityChoices[stat as AbilityScore];
              const isDisabled =
                !isSelected && selectedAbilityCount >= asiRules.count;

              return (
                <label key={stat}>
                  <input type="checkbox" checked={isSelected}>
                    {stat.toUpperCase()}
                  </input>
                </label>
              );
            })}
          </div>
        </div>
      )}

      {/* --- SECTION B: Language Choices --- */}
      {languageChoiceCount > 0 && (
        <div>
          <h3>
            Additional Languages (Choose {languageChoiceCount})
          </h3>
        </div>
      )}

      {/* --- SECTION C: Trait Choices --- */}
      {traitRequiringChoices.length > 0 && (
        <div>
          {traitRequiringChoices.map((effect, idx) => (
            <div>
              <h3>
                {effect.source_trait_name}
                <span>
                  (Choose {effect.choice?.count} {effect.choice?.category}s)
                </span>
              </h3>
            </div>
          ))}
        </div>
      )}

      {/* Empty State Fallback */}
      {!asiRules && languageChoiceCount === 0 && traitRequiringChoices.length === 0 && (
        <p>No choices required for this race.</p>
      )}
    </div>
  );
};
