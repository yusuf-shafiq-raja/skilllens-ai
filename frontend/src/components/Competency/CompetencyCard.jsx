function CompetencyCard({
  title,
  value = 0,
  level = "N/A",
}) {

  function getColor() {

    if (value >= 90) return "bg-green-500";

    if (value >= 70) return "bg-blue-500";

    if (value >= 50) return "bg-yellow-500";

    return "bg-red-500";
  }

  return (

    <div className="bg-white rounded-2xl shadow-md p-6">

      <p className="text-gray-500 text-lg">

        {title}

      </p>

      <h2 className="text-4xl font-bold mt-3">

        {value}%

      </h2>

      <div className="w-full bg-gray-200 rounded-full h-3 mt-5">

        <div
          className={`${getColor()} h-3 rounded-full transition-all duration-500`}
          style={{
            width: `${value}%`,
          }}
        />

      </div>

      <p className="mt-4 text-blue-600 font-semibold">

        {level}

      </p>

    </div>

  );

}

export default CompetencyCard;