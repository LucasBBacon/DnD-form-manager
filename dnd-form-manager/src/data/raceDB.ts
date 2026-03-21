import type { Race } from "../types/types";

const rawRaceFiles = import.meta.glob<{ default: Record<string, Race> }>(
  "../assets/resources/races/*.json",
  { eager: true },
);

export const raceDB: Record<string, Race> = Object.values(rawRaceFiles).reduce(
  (acc, module) => {
    return { ...acc, ...module.default };
  },
  {} as Record<string, Race>,
);

export default raceDB;