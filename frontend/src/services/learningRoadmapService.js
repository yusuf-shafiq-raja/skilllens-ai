import api from "./api";

export async function getLatestLearningRoadmap() {

  const response = await api.get(
    "/learning-roadmap/latest"
  );

  return response.data;

}