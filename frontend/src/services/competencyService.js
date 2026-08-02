import api from "./api";

export const getLatestCompetencyScores = async () => {
  const response = await api.get("/competency-scores/latest");
  return response.data;
};