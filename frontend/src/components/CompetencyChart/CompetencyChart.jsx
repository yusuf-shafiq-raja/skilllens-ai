import { useEffect, useState } from "react";

import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
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
      const result = await getLatestCompetencyScores();

      // No completed assessment yet
      if (!result || result.length === 0) {
        setData([]);
        return;
      }

      const formatted = result.map((item) => ({
        competency: item.competency_name || `Competency ${item.competency_id}`,
        percentage: item.percentage,
      }));

      setData(formatted);
    } catch (error) {
      console.error(error);
      setData([]);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="bg-white rounded-2xl shadow-md p-6 mt-8">
        <h2 className="text-2xl font-bold mb-6">
          Competency Performance
        </h2>

        <p className="text-gray-500">
          Loading competency data...
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
          <p className="text-gray-500 text-lg">
            Complete your first assessment to view competency analytics.
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

      <ResponsiveContainer width="100%" height={350}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="competency" />

          <YAxis domain={[0, 100]} />

          <Tooltip />

          <Bar
            dataKey="percentage"
            radius={[8, 8, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default CompetencyChart;