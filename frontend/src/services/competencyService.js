import api from "./api";

export async function getLatestCompetencyScores() {
  const response = await api.get("/competency-scores/latest");
  return response.data;
}

export async function getCompetencyHistory() {
  const response = await api.get("/competency-scores/history");
  return response.data;
}