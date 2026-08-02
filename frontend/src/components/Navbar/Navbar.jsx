import { useAuth } from "../../context/AuthContext";

function Navbar() {

  const { logout } = useAuth();

  return (

    <header className="bg-white shadow px-8 py-4 flex justify-between items-center">

      <h2 className="text-2xl font-bold">
        Dashboard
      </h2>

      <button
        onClick={logout}
        className="bg-red-500 text-white px-5 py-2 rounded-xl hover:bg-red-600"
      >
        Logout
      </button>

    </header>

  );

}

export default Navbar;