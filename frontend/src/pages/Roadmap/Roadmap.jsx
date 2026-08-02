import { useEffect, useState } from "react";

import MainLayout from "../../layouts/MainLayout";

import RoadmapCard from "../../components/Roadmap/RoadmapCard";

import { getLatestLearningRoadmap }

from "../../services/learningRoadmapService";

function Roadmap() {

  const [roadmaps, setRoadmaps] = useState([]);

  const [loading, setLoading] = useState(true);

  useEffect(() => {

    loadRoadmap();

  }, []);

  async function loadRoadmap() {

    try {

      const data =

        await getLatestLearningRoadmap();

      setRoadmaps(data);

    }

    catch (error) {

      console.error(error);

    }

    finally {

      setLoading(false);

    }

  }

  return (

    <MainLayout>

      <h1 className="text-3xl font-bold mb-8">

        Learning Roadmap

      </h1>

      {

        loading ?

        (

          <p>

            Loading...

          </p>

        )

        :

        roadmaps.map(

          (item) => (

            <div
              key={item.competency}
              className="mb-8"
            >

              <RoadmapCard

                competency={item.competency}

                percentage={item.percentage}

                level={item.level}

                studyTopics={item.study_topics}

                practiceTasks={item.practice_tasks}

                nextLearning={item.next_learning}

              />

            </div>

          )

        )

      }

    </MainLayout>

  );

}

export default Roadmap;