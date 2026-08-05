import { useEffect, useState } from "react";

import Sidebar from "../../components/Sidebar/Sidebar";
import Navbar from "../../components/Navbar/Navbar";

import {
  getPlacementReadiness,
} from "../../services/placementReadinessService";

function PlacementReadiness() {

  const [data, setData] = useState(null);

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadPlacementReadiness();
  }, []);

  const loadPlacementReadiness = async () => {

    try {

      const response =
        await getPlacementReadiness();

      setData(response);

    } catch (error) {

      console.error(error);

    } finally {

      setLoading(false);

    }
  };

  return (

    <div className="flex bg-slate-100 min-h-screen">

      <Sidebar />

      <div className="flex-1">

        <Navbar />

        <div className="p-10">

          <h1 className="text-5xl font-bold mb-8">
            Placement Readiness
          </h1>

          {loading && (

            <div className="bg-white rounded-2xl shadow p-8">

              Loading...

            </div>

          )}

          {!loading && !data && (

            <div className="bg-white rounded-2xl shadow p-8">

              No Placement Readiness Data

            </div>

          )}

          {!loading && data && (

            <div className="bg-white rounded-2xl shadow p-8">

              <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">

                <div>
                  <h3 className="text-gray-500">
                    Overall Score
                  </h3>

                  <p className="text-5xl font-bold text-blue-600 mt-2">
                    {data.overall_score}%
                  </p>
                </div>

                <div>
                  <h3 className="text-gray-500">
                    Resume Score
                  </h3>

                  <p className="text-4xl font-bold mt-2">
                    {data.resume_score}%
                  </p>
                </div>

                <div>
                  <h3 className="text-gray-500">
                    Assessment Score
                  </h3>

                  <p className="text-4xl font-bold mt-2">
                    {data.assessment_score}%
                  </p>
                </div>

                <div>
                  <h3 className="text-gray-500">
                    Competency Score
                  </h3>

                  <p className="text-4xl font-bold mt-2">
                    {data.competency_score}%
                  </p>
                </div>

              </div>

              <hr className="my-8" />

              <div>

                <h2 className="text-2xl font-bold mb-3">
                  Readiness Level
                </h2>

                <p className="text-xl text-green-600 font-semibold">
                  {data.readiness_level}
                </p>

              </div>

              <div className="mt-8">

                <h2 className="text-2xl font-bold mb-3">
                  Recommendation
                </h2>

                <p className="text-gray-700">
                  {data.recommendation}
                </p>

              </div>

            </div>

          )}

        </div>

      </div>

    </div>

  );

}

export default PlacementReadiness;