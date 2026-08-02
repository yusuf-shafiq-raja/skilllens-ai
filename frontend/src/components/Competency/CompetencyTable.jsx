function CompetencyTable({ competencies }) {

  function getLevel(score) {

    if (score >= 90) return "Expert";

    if (score >= 70) return "Advanced";

    if (score >= 50) return "Intermediate";

    return "Beginner";

  }

  function getColor(score) {

    if (score >= 90) return "bg-green-500";

    if (score >= 70) return "bg-blue-500";

    if (score >= 50) return "bg-yellow-500";

    return "bg-red-500";

  }

  if (!competencies || competencies.length === 0) {

    return (

      <div className="bg-white rounded-2xl shadow-md p-6 mt-8">

        <h2 className="text-2xl font-bold">

          Competency Breakdown

        </h2>

        <p className="text-gray-500 mt-4">

          No competency data available.

        </p>

      </div>

    );

  }

  return (

    <div className="bg-white rounded-2xl shadow-md p-6 mt-8">

      <h2 className="text-2xl font-bold mb-6">

        Competency Breakdown

      </h2>

      <div className="overflow-x-auto">

        <table className="w-full">

          <thead>

            <tr className="border-b">

              <th className="text-left py-3">
                Competency
              </th>

              <th className="text-center py-3">
                Correct
              </th>

              <th className="text-center py-3">
                Questions
              </th>

              <th className="text-center py-3">
                Level
              </th>

              <th className="text-right py-3">
                Progress
              </th>

            </tr>

          </thead>

          <tbody>

            {competencies.map((item) => (

              <tr
                key={item.competency_id}
                className="border-b hover:bg-slate-50"
              >

                <td className="py-5 font-semibold">

                  {item.competency_name}

                </td>

                <td className="text-center">

                  {item.correct_answers}

                </td>

                <td className="text-center">

                  {item.total_questions}

                </td>

                <td className="text-center">

                  <span
                    className={`text-white px-3 py-1 rounded-full text-sm ${getColor(item.percentage)}`}
                  >

                    {getLevel(item.percentage)}

                  </span>

                </td>

                <td>

                  <div className="flex items-center gap-3">

                    <div className="w-full bg-gray-200 rounded-full h-3">

                      <div
                        className={`${getColor(item.percentage)} h-3 rounded-full transition-all duration-700`}
                        style={{
                          width: `${item.percentage}%`,
                        }}
                      />

                    </div>

                    <span className="font-bold w-14 text-right">

                      {item.percentage}%

                    </span>

                  </div>

                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </div>

  );

}

export default CompetencyTable;