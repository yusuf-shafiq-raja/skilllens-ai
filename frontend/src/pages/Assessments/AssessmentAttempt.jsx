import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import MainLayout from "../../layouts/MainLayout";

import Card from "../../components/Card/Card";
import Button from "../../components/Button/Button";

import {
  getAttemptDetails,
  submitAnswer,
  submitAssessment,
} from "../../services/assessmentService";

function AssessmentAttempt() {

  const { attemptId } = useParams();

  const navigate = useNavigate();

  const [attempt, setAttempt] = useState(null);

  const [currentQuestion, setCurrentQuestion] = useState(0);

  const [selectedAnswer, setSelectedAnswer] = useState("");

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAttempt();
  }, []);

  async function loadAttempt() {

    try {

      const data = await getAttemptDetails(attemptId);

      setAttempt(data);

    } catch (error) {

      console.error(error);

    } finally {

      setLoading(false);

    }

  }

  async function handleNext() {

    if (!selectedAnswer) {

      alert("Please select an answer.");

      return;

    }

    try {

      const question =
        attempt.questions[currentQuestion];

      await submitAnswer(
        attemptId,
        question.id,
        selectedAnswer
      );

      setSelectedAnswer("");

      if (
        currentQuestion <
        attempt.questions.length - 1
      ) {

        setCurrentQuestion(
          currentQuestion + 1
        );

      }

      else {

        await submitAssessment(
          attemptId
        );

        navigate(
          `/result/${attemptId}`
        );

      }

    }

    catch (error) {

      console.error(error);

      alert("Unable to submit answer.");

    }

  }

  if (loading) {

    return (

      <MainLayout>

        <h2 className="text-2xl font-bold">

          Loading Assessment...

        </h2>

      </MainLayout>

    );

  }

  if (!attempt) {

    return (

      <MainLayout>

        <h2 className="text-2xl font-bold">

          Assessment not found.

        </h2>

      </MainLayout>

    );

  }

  const question =
    attempt.questions[currentQuestion];

  return (

    <MainLayout>

      <Card>

        <h1 className="text-3xl font-bold">

          {attempt.assessment.title}

        </h1>

        <p className="text-gray-500 mt-2">

          Question {currentQuestion + 1} of {attempt.questions.length}

        </p>

        <div className="mt-8">

          <h2 className="text-xl font-semibold mb-6">

            {question.question}

          </h2>

          {["A", "B", "C", "D"].map((option) => {

            const value =
              question[
                `option_${option.toLowerCase()}`
              ];

            return (

              <label
                key={option}
                className="flex items-center gap-4 border rounded-xl p-4 mb-4 cursor-pointer hover:bg-slate-100"
              >

                <input
                  type="radio"
                  checked={
                    selectedAnswer === option
                  }
                  onChange={() =>
                    setSelectedAnswer(option)
                  }
                />

                <span>

                  <strong>{option}.</strong> {value}

                </span>

              </label>

            );

          })}

        </div>

        <div className="mt-8 flex justify-end">

          <Button
            className="w-56"
            onClick={handleNext}
          >

            {

              currentQuestion ===
              attempt.questions.length - 1

                ? "Submit Assessment"

                : "Next Question"

            }

          </Button>

        </div>

      </Card>

    </MainLayout>

  );

}

export default AssessmentAttempt;