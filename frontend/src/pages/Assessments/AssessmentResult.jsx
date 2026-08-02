import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import MainLayout from "../../layouts/MainLayout";

import Card from "../../components/Card/Card";
import Button from "../../components/Button/Button";

import { getResult } from "../../services/assessmentService";

function AssessmentResult() {

  const { attemptId } = useParams();

  const navigate = useNavigate();

  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadResult();
  }, []);

  async function loadResult() {

    try {

      const data = await getResult(attemptId);

      setResult(data);

    } catch (error) {

      console.error(error);

    } finally {

      setLoading(false);

    }

  }

  if (loading) {

    return (
      <MainLayout>
        <h2 className="text-2xl font-bold">
          Loading Result...
        </h2>
      </MainLayout>
    );

  }

  if (!result) {

    return (
      <MainLayout>
        <h2 className="text-2xl font-bold">
          Result not found.
        </h2>
      </MainLayout>
    );

  }

  return (

    <MainLayout>

      <div className="max-w-3xl mx-auto">

        <Card>

          <h1 className="text-4xl font-bold mb-8">
            Assessment Completed 🎉
          </h1>

          <div className="grid grid-cols-2 gap-6">

            <div className="bg-slate-100 rounded-xl p-5">
              <p className="text-gray-500">
                Score
              </p>

              <h2 className="text-3xl font-bold mt-2">
                {result.score}
              </h2>
            </div>

            <div className="bg-slate-100 rounded-xl p-5">
              <p className="text-gray-500">
                Total Marks
              </p>

              <h2 className="text-3xl font-bold mt-2">
                {result.total_marks}
              </h2>
            </div>

            <div className="bg-slate-100 rounded-xl p-5">
              <p className="text-gray-500">
                Percentage
              </p>

              <h2 className="text-3xl font-bold mt-2">
                {result.percentage}%
              </h2>
            </div>

            <div className="bg-slate-100 rounded-xl p-5">
              <p className="text-gray-500">
                Status
              </p>

              <h2
                className={`text-3xl font-bold mt-2 ${
                  result.status === "PASSED"
                    ? "text-green-600"
                    : "text-red-600"
                }`}
              >
                {result.status}
              </h2>
            </div>

          </div>

          <div className="mt-10">

            <Button
              onClick={() => navigate("/dashboard")}
            >
              Return to Dashboard
            </Button>

          </div>

        </Card>

      </div>

    </MainLayout>

  );

}

export default AssessmentResult;