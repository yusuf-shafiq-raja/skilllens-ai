import { NavLink } from "react-router-dom";

import {
  LayoutDashboard,
  ClipboardList,
  Brain,
  BookOpen,
  FileText,
  Briefcase,
} from "lucide-react";

function Sidebar() {
  const menu = [
    {
      name: "Dashboard",
      path: "/dashboard",
      icon: <LayoutDashboard size={20} />,
    },
    {
      name: "Assessments",
      path: "/assessments",
      icon: <ClipboardList size={20} />,
    },
    {
      name: "Competency",
      path: "/competency",
      icon: <Brain size={20} />,
    },
    {
      name: "Roadmap",
      path: "/roadmap",
      icon: <BookOpen size={20} />,
    },
    {
      name: "Placement",
      path: "/placement-readiness",
      icon: <Briefcase size={20} />,
    },
    {
      name: "Resume",
      path: "/resume",
      icon: <FileText size={20} />,
    },
  ];

  return (
    <aside className="w-64 min-h-screen bg-slate-900 text-white p-6">
      <h1 className="text-3xl font-bold mb-10">
        SkillLens AI
      </h1>

      <div className="space-y-2">
        {menu.map((item) => (
          <NavLink
            key={item.name}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 p-3 rounded-xl transition ${
                isActive
                  ? "bg-blue-600"
                  : "hover:bg-slate-800"
              }`
            }
          >
            {item.icon}
            <span>{item.name}</span>
          </NavLink>
        ))}
      </div>
    </aside>
  );
}

export default Sidebar;