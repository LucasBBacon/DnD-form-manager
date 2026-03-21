import type { Subrace } from "../types/types";

const rawSubraceFiles = import.meta.glob<{ default: Record<string, Subrace> }>(
  "../assets/resources/subraces/*.json",
  { eager: true },
);

export const subraceDB: Record<string, Subrace> = Object.values(rawSubraceFiles).reduce(
  (acc, module) => {
    return { ...acc, ...module.default };
  },
  {} as Record<string, Subrace>,
);

export default subraceDB;