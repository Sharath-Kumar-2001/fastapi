// src/routes/root.tsx  (or wherever your home page file is)
import { Link } from "react-router";

export default function Home() {
  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center px-8 relative overflow-hidden">
      
      {/* Full-screen futuristic background */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-900 via-black to-blue-900 -z-10"></div>

      {/* Content */}
      <div className="text-center z-10">

        {/* Logo */}
        <div className="flex items-center justify-center gap-4 mb-16">
          <div className="w-16 h-16 bg-gradient-to-r from-cyan-400 to-purple-600 rounded-2xl flex items-center justify-center text-3xl font-bold">
            J
          </div>
          <h1 className="text-5xl font-bold text-cyan-400">Jobify</h1>
        </div>

        {/* Catchphrase */}
        <h2 className="text-6xl md:text-8xl font-extrabold leading-tight">
          Your Next Job
          <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400">
            Starts Here
          </span>
        </h2>

        <p className="text-xl md:text-2xl text-gray-300 mt-8">
          Find dream jobs. Apply in seconds. Get hired faster.
        </p>

        {/* Button */}
        <div className="mt-12">
          <Link
            to="/job-boards"
            className="inline-block px-16 py-6 bg-gradient-to-r from-cyan-500 to-purple-600 text-2xl font-bold rounded-full 
                       hover:scale-110 hover:shadow-2xl hover:shadow-purple-500/50 transition duration-300"
          >
            Explore Jobs Now
          </Link>
        </div>

        <p className="mt-10 text-gray-400">
          Have an account? <Link to="/login" className="text-cyan-400 hover:underline">Sign in</Link>
        </p>
      </div>
    </div>
  );
}