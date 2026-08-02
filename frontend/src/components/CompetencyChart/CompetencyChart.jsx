import { useEffect, useState } from "react";

import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Cell,
} from "recharts";

import { getLatestCompetencyScores } from "../../services/competencyService";

function CompetencyChart() {

  const [data, setData] = useState([]);

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCompetencies();
  }, []);

  async function loadCompetencies() {

    try {

      const result =
        await getLatestCompetencyScores();

      if (!result || result.length === 0) {

        setData([]);

        return;

      }

      const formatted = result.map((item) => ({

        competency: item.competency_name,

        percentage: item.percentage,

      }));

      setData(formatted);

    }

    catch (error) {

      console.error(error);

    }

    finally {

      setLoading(false);

    }

  }

  function getColor(value) {

    if (value >= 90)
      return "#22c55e";

    if (value >= 70)
      return "#3b82f6";

    if (value >= 50)
      return "#f59e0b";

    return "#ef4444";

  }

  if (loading) {

    return (

      <div className="bg-white rounded-2xl shadow-md p-6 mt-8">

        <h2 className="text-2xl font-bold mb-6">

          Competency Performance

        </h2>

        <p className="text-gray-500">

          Loading...

        </p>

      </div>

    );

  }

  if (data.length === 0) {

    return (

      <div className="bg-white rounded-2xl shadow-md p-6 mt-8">

        <h2 className="text-2xl font-bold mb-6">

          Competency Performance

        </h2>

        <div className="h-72 flex items-center justify-center border-2 border-dashed rounded-xl">

          <p className="text-gray-500">

            Complete an assessment first.

          </p>

        </div>

      </div>

    );

  }

  return (

    <div className="bg-white rounded-2xl shadow-md p-6 mt-8">

      <h2 className="text-2xl font-bold mb-6">

        Competency Performance

      </h2>

      <ResponsiveContainer
        width="100%"
        height={350}
      >

        <BarChart data={data}>

          <CartesianGrid strokeDasharray="3 3" />

          <XAxis
            dataKey="competency"
          />

          <YAxis
            domain={[0, 100]}
          />

          <Tooltip />

          <Bar
            dataKey="percentage"
            radius={[8, 8, 0, 0]}
          >

            {

              data.map(

                (entry, index) => (

                  <Cell
                    key={index}
                    fill={getColor(entry.percentage)}
                  />

                )

              )

            }

          </Bar>

        </BarChart>

      </ResponsiveContainer>

    </div>

  );

}

export default CompetencyChart;