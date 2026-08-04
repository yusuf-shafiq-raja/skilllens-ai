import api from "./api";

export const generatePlacementReadiness = async (resumeScore) => {

    const response = await api.post(
        `/placement-readiness/generate/${resumeScore}`
    );

    return response.data;
};

export const getPlacementReadiness = async () => {

    const response = await api.get(
        "/placement-readiness"
    );

    return response.data;
};