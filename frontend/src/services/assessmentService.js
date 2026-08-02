import api from "./api";

// --------------------------------------------
// Get All Assessments
// --------------------------------------------

export const getAssessments = async () => {
  const response = await api.get("/assessments");
  return response.data;
};

// --------------------------------------------
// Start Assessment
// --------------------------------------------

export const startAssessment = async (assessmentId) => {
  const response = await api.post(
    `/assessment-attempts/start/${assessmentId}`
  );

  return response.data;
};

// --------------------------------------------
// Get Attempt Details
// --------------------------------------------

export const getAttemptDetails = async (attemptId) => {
  const response = await api.get(
    `/assessment-attempts/${attemptId}/details`
  );

  return response.data;
};

// --------------------------------------------
// Submit Answer
// --------------------------------------------

export const submitAnswer = async (
  attemptId,
  questionId,
  selectedAnswer
) => {
  const response = await api.post(
    `/assessment-attempts/${attemptId}/answer`,
    {
      question_id: questionId,
      selected_answer: selectedAnswer,
    }
  );

  return response.data;
};

// --------------------------------------------
// Submit Assessment
// --------------------------------------------

export const submitAssessment = async (attemptId) => {
  const response = await api.post(
    `/assessment-attempts/${attemptId}/submit`
  );

  return response.data;
};

// --------------------------------------------
// Get Result
// --------------------------------------------

export const getResult = async (attemptId) => {
  const response = await api.get(
    `/assessment-attempts/${attemptId}`
  );

  return response.data;
};