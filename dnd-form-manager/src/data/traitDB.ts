import type { Trait } from "../types/types";

const rawTraitFiles = import.meta.glob<{ default: Record<string, Trait> }>(
  "../assets/resources/traits/*.json",
  { eager: true },
);

export const traitDB: Record<string, Trait> = Object.values(rawTraitFiles).reduce(
  (acc, module) => {
    return { ...acc, ...module.default };
  },
  {} as Record<string, Trait>,
);

export default traitDB;