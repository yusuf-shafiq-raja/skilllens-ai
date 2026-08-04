import { useState } from "react";
import { useNavigate } from "react-router-dom";

import MainLayout from "../../layouts/MainLayout";
import Card from "../../components/Card/Card";
import Button from "../../components/Button/Button";

import { uploadResume } from "../../services/resumeService";
import {
  generatePlacementReadiness
} from "../../services/placementReadinessService";
import { startAssessment } from "../../services/assessmentService";



function Resume() {

  const navigate = useNavigate();

  const [file, setFile] = useState(null);

  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(false);

  async function handleUpload() {

    if (!file) {

      alert("Please select a PDF.");

      return;

    }

    try {

      setLoading(true);

      const data = await uploadResume(file);

setResult(data);

// Generate Placement Readiness
await generatePlacementReadiness(
  data.readiness_score
);

    }

    catch (error) {

      console.error(error);

      alert("Resume upload failed.");

    }

    finally {

      setLoading(false);

    }

  }

  async function handleStartAssessment(
    assessmentId
  ) {

    try {

      const result = await startAssessment(
        assessmentId
      );

      navigate(
        `/assessment/${result.attempt_id}`
      );

    }

    catch (error) {

      console.error(error);

      alert("Unable to start assessment.");

    }

  }

  return (

    <MainLayout>

      <Card>

        <h1 className="text-3xl font-bold">

          Resume Analyzer

        </h1>

        <p className="text-gray-500 mt-2">

          Upload your resume to detect your skills and receive personalized assessments.

        </p>

        <input
          type="file"
          accept=".pdf"
          className="mt-8"
          onChange={(e) =>
            setFile(e.target.files[0])
          }
        />

        <div className="mt-6">

          <Button
            onClick={handleUpload}
            disabled={loading}
          >

            {

              loading

                ? "Analyzing..."

                : "Upload Resume"

            }

          </Button>

        </div>

      </Card>

      {

        result && (

          <Card className="mt-8">

            <h2 className="text-2xl font-bold">

              Resume Analysis

            </h2>

            <div className="mt-6">

              <h3 className="font-semibold">

                Resume Readiness

              </h3>

              <p className="text-4xl font-bold text-blue-600 mt-2">

                {result.readiness_score}%

              </p>

            </div>

            <div className="mt-8">

              <h3 className="font-semibold">

                Skills Detected

              </h3>

              <div className="flex flex-wrap gap-3 mt-4">

                {

                  result.matched_skills.map(

                    (skill) => (

                      <span
                        key={skill}
                        className="bg-green-100 text-green-700 px-4 py-2 rounded-full font-medium"
                      >

                        ✅ {skill}

                      </span>

                    )

                  )

                }

              </div>

            </div>

            <div className="mt-8">

              <h3 className="font-semibold">

                Skills Missing

              </h3>

              <div className="flex flex-wrap gap-3 mt-4">

                {

                  result.missing_skills.map(

                    (skill) => (

                      <span
                        key={skill}
                        className="bg-red-100 text-red-700 px-4 py-2 rounded-full font-medium"
                      >

                        ❌ {skill}

                      </span>

                    )

                  )

                }

              </div>

            </div>

            <div className="mt-10">

              <h3 className="text-2xl font-bold">

                Recommended Assessments

              </h3>

              {

                result.recommended_assessments.length === 0

                  ? (

                    <p className="text-gray-500 mt-4">

                      No assessments available for the detected skills.

                    </p>

                  )

                  : (

                    result.recommended_assessments.map(

                      (assessment) => (

                        <div
                          key={assessment.id}
                          className="border rounded-xl p-6 mt-5 shadow-sm"
                        >

                          <h4 className="text-xl font-bold">

                            {assessment.title}

                          </h4>

                          <p className="text-gray-600 mt-2">

                            {assessment.description}

                          </p>

                          <div className="flex gap-8 mt-4 text-gray-500">

                            <span>

                              ⏱ {assessment.duration_minutes} Minutes

                            </span>

                            <span>

                              🎯 Passing Score : {assessment.passing_score}%

                            </span>

                          </div>

                          <Button
                            className="mt-6"
                            onClick={() =>
                              handleStartAssessment(
                                assessment.id
                              )
                            }
                          >

                            Start Assessment

                          </Button>

                        </div>

                      )

                    )

                  )

              }

            </div>

          </Card>

        )

      }

    </MainLayout>

  );

}

export default Resume;