import { useEffect, useState } from "react";

import MainLayout from "../../layouts/MainLayout";

import DashboardCard from "../../components/DashboardCard/DashboardCard";
import CompetencyChart from "../../components/CompetencyChart/CompetencyChart";

import { getDashboard } from "../../services/dashboardService";

function Dashboard() {

  const [dashboard, setDashboard] = useState(null);

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboard();
  }, []);

  async function loadDashboard() {

    try {

      const data = await getDashboard();

      setDashboard(data);

    } catch (error) {

      console.error(error);

    } finally {

      setLoading(false);

    }

  }

  if (loading) {

    return (
      <MainLayout>

        <div className="text-2xl font-bold">
          Loading Dashboard...
        </div>

      </MainLayout>
    );

  }

  return (

    <MainLayout>

      <h1 className="text-4xl font-bold">
        Welcome {dashboard.user_name} 👋
      </h1>

      <p className="text-gray-500 mt-2">
        Here's your SkillLens overview.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 mt-10">

        <DashboardCard
          title="Assessments"
          value={dashboard.completed_assessments}
        />

        <DashboardCard
          title="Average Score"
          value={`${dashboard.average_score}%`}
        />

        <DashboardCard
          title="Latest Score"
          value={`${dashboard.latest_score}%`}
        />

        <DashboardCard
          title="Top Competency"
          value={dashboard.top_competency}
        />

        <DashboardCard
          title="Weakest Competency"
          value={dashboard.weakest_competency}
        />

        <DashboardCard
          title="Resume Readiness"
          value={`${dashboard.resume_readiness}%`}
        />

      </div>

      <CompetencyChart />

    </MainLayout>

  );

}

export default Dashboard;