import { describe, expect, it } from "vitest";
import { calculateModifier, calculateStats } from "./statUtils";
import type { ActiveEffect, MergedRaceData, StatsRecord } from "./types";

describe("calculateModifier", () => {
  it("correctly calculates 5E ability modifiers", () => {
    expect(calculateModifier(10)).toBe(0);
    expect(calculateModifier(15)).toBe(2);
    expect(calculateModifier(16)).toBe(3);
    expect(calculateModifier(8)).toBe(-1);
  });
});

describe("calculateStats", () => {
  const mockBaseStats: StatsRecord = {
    str: 15,
    dex: 14,
    con: 13,
    int: 12,
    wis: 10,
    cha: 8,
  };

  const mockHalfElfRace: Partial<MergedRaceData> = {
    ability_bonuses: {
      fixed: { cha: 2 },
      choices: {
        count: 2,
        bonus: 1,
        options: ["str", "dex", "con", "int", "wis"],
      },
    },
  };

  const mockUserChoices: Partial<StatsRecord> = {
    dex: 1,
    con: 1,
  };

  const mockActiveEffects: ActiveEffect[] = [
    {
      type: "stat_modifier",
      target: "str",
      value: 1,
      source_trait_id: "mock",
      source_trait_name: "Mock",
    },
  ];

  it("should aggregate base, fixed racial, chosen racial, and trait bonuses", () => {
    const finalStats = calculateStats(
      mockBaseStats,
      mockHalfElfRace as MergedRaceData,
      mockUserChoices,
      mockActiveEffects,
    );

    // STR: 15 (base) + 1 (trait) = 16 (mod: +3)
    expect(finalStats.str.score).toBe(16);
    expect(finalStats.str.modifier).toBe(3);

    // DEX: 14 (base) + 1 (choice) = 15 (mod: + 2)
    expect(finalStats.dex.score).toBe(15);

    // CON: 13 (base) + 1 (choice) = 14 (mod: + 2)
    expect(finalStats.con.score).toBe(14);

    // INT: 12 (base) + 0 = 12
    expect(finalStats.int.score).toBe(12);

    // WIS: 10 (base) + 0 = 10
    expect(finalStats.wis.score).toBe(10);

    // CHA: 8 (base) + 2 (fixed) = 10 (mod: 0)
    expect(finalStats.cha.score).toBe(10);
    expect(finalStats.cha.modifier).toBe(0);
  });

  it("should calculate cleanly even if no choices or traits are provided", () => {
    const finalStats = calculateStats(
      mockBaseStats,
      mockHalfElfRace as MergedRaceData,
    );

    // CHA should still get the +2 fixed bonus
    expect(finalStats.cha.score).toBe(10);
    // DEX should just be base 14
    expect(finalStats.dex.score).toBe(14);
  });
});
