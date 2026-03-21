import React from "react";
import { useCharacterStore } from "../store/characterStore";
import raceDB from "../data/raceDB";
import subraceDB from "../data/subraceDB";

export const RaceSelectionScreen = () => {
  const selectedRaceId = useCharacterStore((state) => state.selectedRaceId);
  // const selectedSubraceId = useCharacterStore(
  // (state) => state.selectedSubraceId,
  // );
  const setRace = useCharacterStore((state) => state.setRace);
  const setSubrace = useCharacterStore((state) => state.setSubrace);

  // const mergedRace = useCharacterStore(state => state.getMergedRace());
  // const finalStats = useCharacterStore(state => state.getFinalStats());

  const availableRaces = Object.entries(raceDB);

  return (
    <div className="flex h-screen bg-white">
      {/* --- LEFT COLUMN: Master List */}
      <div className="w-1/3 border-r p-4 overflow-y-auto bg-gray-50">
        <h2 className="text-2xl font-bold mb-4">Choose a Race</h2>
        <div className="flex flex-col gap-2">
          {availableRaces.map(([raceId, race]) => (
            <button
              key={raceId}
              onClick={() => setRace(raceId)}
              className={`p-4 text-left border rounded-lg transition-shadow hover:shadow-md ${
                selectedRaceId === raceId
                  ? "bg-blue-600 text-white border-blue-700"
                  : "bg-white hover:bg-blue-50"
              }`}
            >
              <h3 className="font-bold text-lg">{race.name}</h3>
              <p
                className={`text-sm ${
                  selectedRaceId === raceId ? "text-blue-100" : "text-gray-600"
                }`}
              >
                {race.lore?.short_description || `A standard ${race.name}`}
              </p>
            </button>
          ))}
        </div>
      </div>

      {/* --- RIGHT COLUMN: The Detail View --- */}
      <div className="w-2/3 p-8 overflow-y-auto">
        {!selectedRaceId ? (
          <div className="h-full flex items-center justify-center text-gray-400 italic">
            Select a race from the left to view details.
          </div>
        ) : (
          <div className="max-w-3xl mx-auto space-y-8">
            {/* Race Header and Lore */}
            <div>
              <h1 className="text-4xl font-extrabold mb-2">
                {raceDB[selectedRaceId].name}
              </h1>
              <p className="text-gray-700 leading-relaxed">
                {raceDB[selectedRaceId].lore?.full_text}
              </p>
            </div>

            {/* The Subrace Interceptor */}
            {raceDB[selectedRaceId].subrace_info && (
              <div className="bg-yellow-50 border border-yellow-200 p-4 rounded-lg">
                <h3 className="font-bold text-yellow-800 mb-2">
                  Subrace Required
                </h3>
                <select
                  className="w-full p-2 border rounded"
                  value={selectedRaceId || ""}
                  onChange={(e) => setSubrace(e.target.value)}
                >
                  <option value="" disabled>
                    -- Select a Subrace --
                  </option>
                  {Object.values(subraceDB)
                    .filter((sub) => sub.parent_race_id === selectedRaceId)
                    .map((sub) => (
                      <option 
                        key={sub.id} 
                        value={sub.id}
                      >
                        {sub.name}
                      </option>
                    ))}
                </select>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
