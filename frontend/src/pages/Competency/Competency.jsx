import { useEffect, useState } from "react";

import MainLayout from "../../layouts/MainLayout";

import CompetencyCard from "../../components/Competency/CompetencyCard";
import CompetencyTable from "../../components/Competency/CompetencyTable";
import CompetencyChart from "../../components/CompetencyChart/CompetencyChart";

import {
  getLatestCompetencyScores,
} from "../../services/competencyService";

function Competency() {

  const [competencies, setCompetencies] = useState([]);

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCompetencies();
  }, []);

  async function loadCompetencies() {

    try {

      const data =
        await getLatestCompetencyScores();

      setCompetencies(data);

    }

    catch (error) {

      console.error(error);

    }

    finally {

      setLoading(false);

    }

  }

  function getLevel(score) {

    if (score >= 90)
      return "Expert";

    if (score >= 70)
      return "Advanced";

    if (score >= 50)
      return "Intermediate";

    return "Beginner";
  }

  if (loading) {

    return (

      <MainLayout>

        <h1 className="text-3xl font-bold">

          Loading...

        </h1>

      </MainLayout>

    );

  }

  if (competencies.length === 0) {

    return (

      <MainLayout>

        <h1 className="text-3xl font-bold mb-8">

          Competency Dashboard

        </h1>

        <div className="bg-white rounded-2xl shadow-md p-10">

          <h2 className="text-xl font-semibold">

            No competency data available.

          </h2>

          <p className="text-gray-500 mt-3">

            Complete an assessment first.

          </p>

        </div>

      </MainLayout>

    );

  }

  const average = Math.round(

    competencies.reduce(

      (sum, item) => sum + item.percentage,

      0

    ) / competencies.length

  );

  const strongest =
    [...competencies].sort(

      (a, b) => b.percentage - a.percentage

    )[0];

  const weakest =
    [...competencies].sort(

      (a, b) => a.percentage - b.percentage

    )[0];

  return (

    <MainLayout>

      <h1 className="text-3xl font-bold mb-8">

        Competency Dashboard

      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">

        <CompetencyCard
          title="Average Score"
          value={average}
          level={getLevel(average)}
        />

        <CompetencyCard
          title="Strongest Competency"
          value={strongest.percentage}
          level={strongest.competency_name}
        />

        <CompetencyCard
          title="Weakest Competency"
          value={weakest.percentage}
          level={weakest.competency_name}
        />

        <CompetencyCard
          title="Competencies"
          value={competencies.length}
          level="Tracked"
        />

      </div>

      <CompetencyChart />

      <CompetencyTable
        competencies={competencies}
      />

    </MainLayout>

  );

}

export default Competency;