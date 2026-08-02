import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import MainLayout from "../../layouts/MainLayout";

import Card from "../../components/Card/Card";
import Button from "../../components/Button/Button";

import {
  getAssessments,
  startAssessment,
} from "../../services/assessmentService";

function AssessmentList() {

  const navigate = useNavigate();

  const [assessments, setAssessments] = useState([]);

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAssessments();
  }, []);

  async function loadAssessments() {

    try {

      const data = await getAssessments();

      setAssessments(data);

    } catch (error) {

      console.error(error);

    } finally {

      setLoading(false);

    }

  }

  async function handleStart(id) {

    try {

      const response = await startAssessment(id);

      navigate(`/assessment/${response.attempt_id}`);

    } catch (error) {

      alert(
        error.response?.data?.detail ||
        "Unable to start assessment."
      );

    }

  }

  if (loading) {

    return (

      <MainLayout>

        <h2 className="text-2xl font-bold">
          Loading Assessments...
        </h2>

      </MainLayout>

    );

  }

  return (

    <MainLayout>

      <h1 className="text-4xl font-bold mb-8">
        Assessments
      </h1>

      {assessments.length === 0 ? (

        <Card>

          <p className="text-gray-600">
            No assessments available.
          </p>

        </Card>

      ) : (

        <div className="grid gap-6">

          {assessments.map((assessment) => (

            <Card key={assessment.id}>

              <h2 className="text-2xl font-bold">
                {assessment.title}
              </h2>

              <p className="text-gray-600 mt-2">
                {assessment.description}
              </p>

              <div className="grid grid-cols-2 gap-4 mt-6 text-sm text-gray-500">

                <div>
                  <strong>Duration:</strong>{" "}
                  {assessment.duration_minutes} mins
                </div>

                <div>
                  <strong>Passing Score:</strong>{" "}
                  {assessment.passing_score}%
                </div>

              </div>

              <div className="mt-8">

                <Button
                  onClick={() =>
                    handleStart(assessment.id)
                  }
                >
                  Start Assessment
                </Button>

              </div>

            </Card>

          ))}

        </div>

      )}

    </MainLayout>

  );

}

export default AssessmentList;