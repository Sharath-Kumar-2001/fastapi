// src/routes/DefaultLayout.tsx  (or wherever it is)
import { NavLink, Outlet } from "react-router";

export default function DefaultLayout() {
  return (
    <div className="min-h-screen bg-black text-white relative">
      {/* Futuristic background */}
      <div className="fixed inset-0 bg-gradient-to-br from-purple-900 via-black to-blue-900 -z-10"></div>

      {/* Beautiful Nav Bar */}
      <nav className="relative z-50 backdrop-blur-xl bg-black/50 border-b border-white/10">
        <div className="max-w-7xl mx-auto px-8 py-6 flex justify-between items-center">
          <div className="flex items-center gap-8">
            {/* Logo */}
            <NavLink to="/" className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-r from-cyan-400 to-purple-600 rounded-xl flex items-center justify-center font-bold text-xl">
                J
              </div>
              <span className="text-2xl font-bold text-cyan-400">Jobify</span>
            </NavLink>

            {/* Nav Links */}
            <div className="hidden md:flex gap-8">
              <NavLink
                to="/job-boards"
                className={({ isActive }) =>
                  `text-lg font-medium transition ${isActive ? "text-cyan-400" : "text-gray-300 hover:text-white"}`
                }
              >
                Job Boards
              </NavLink>
            </div>
          </div>

          {/* Right side */}
          <div className="flex gap-4">
            <NavLink to="/login" className="text-gray-300 hover:text-white">
              Sign In
            </NavLink>
            <NavLink
              to="/register"
              className="px-5 py-2 bg-gradient-to-r from-cyan-500 to-purple-600 rounded-full font-medium hover:scale-105 transition"
            >
              Get Started
            </NavLink>
          </div>
        </div>
      </nav>

      {/* Page Content */}
      <div className="relative z-10">
        <Outlet />
      </div>
    </div>
  );
}