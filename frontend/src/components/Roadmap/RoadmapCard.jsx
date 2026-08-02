function RoadmapCard({

  competency,

  percentage,

  level,

  studyTopics,

  practiceTasks,

  nextLearning

}) {

  const levelColor =

    level === "Strong"

      ? "text-green-600"

      : level === "Average"

      ? "text-yellow-600"

      : "text-red-600";

  return (

    <div className="bg-white rounded-2xl shadow-md p-6">

      <div className="flex justify-between items-center">

        <h2 className="text-2xl font-bold">

          {competency}

        </h2>

        <div className="text-right">

          <p className="text-2xl font-bold">

            {percentage}%

          </p>

          <p className={`${levelColor} font-semibold`}>

            {level}

          </p>

        </div>

      </div>

      <div className="mt-6">

        <h3 className="font-semibold">

          Study Topics

        </h3>

        <ul className="list-disc ml-6 mt-3">

          {

            studyTopics.map(

              (topic) => (

                <li key={topic}>

                  {topic}

                </li>

              )

            )

          }

        </ul>

      </div>

      <div className="mt-6">

        <h3 className="font-semibold">

          Practice

        </h3>

        <ul className="list-disc ml-6 mt-3">

          {

            practiceTasks.map(

              (task) => (

                <li key={task}>

                  {task}

                </li>

              )

            )

          }

        </ul>

      </div>

      <div className="mt-6">

        <h3 className="font-semibold">

          Next Learning

        </h3>

        <p className="text-blue-600 mt-2 font-semibold">

          {nextLearning}

        </p>

      </div>

    </div>

  );

}

export default RoadmapCard;