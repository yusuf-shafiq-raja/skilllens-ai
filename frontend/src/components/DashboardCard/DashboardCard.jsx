function DashboardCard({
  title,
  value,
}) {
  return (
    <div className="bg-white rounded-2xl shadow-md p-6 hover:shadow-xl transition">

      <h3 className="text-gray-500 text-sm">
        {title}
      </h3>

      <h2 className="text-3xl font-bold mt-3 text-slate-800">
        {value}
      </h2>

    </div>
  );
}

export default DashboardCard;