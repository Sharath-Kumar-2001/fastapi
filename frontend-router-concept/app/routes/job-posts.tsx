import { Link } from "react-router";
import type { Route } from "../+types/root";

export async function clientLoader({ params }: Route.LoaderArgs) {
    const res = await fetch(`/api/job-boards/${params.jobBoardId}/job-posts`);
    const jobPosts = await res.json();
    return jobPosts
}

export default function JobPosts({loaderData}: Route.ComponentProps) {
  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Job Posts</h1>
        
        <div className="space-y-6">
          {loaderData?.map((job) => (
            <div 
              key={job.id} 
              className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
            >
              <div className="flex justify-between items-start mb-4">
                <h2 className="text-2xl font-semibold text-gray-800">
                  {job.job_title}
                </h2>
                <span className="text-sm text-gray-500 bg-gray-100 px-3 py-1 rounded-full">
                  ID: {job.id}
                </span>
              </div>
              
              <p className="text-gray-600 mb-4 leading-relaxed">
                {job.job_description}
              </p>
              
              <div className="flex items-center text-sm text-gray-500">
                <svg 
                  className="w-4 h-4 mr-2" 
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path 
                    strokeLinecap="round" 
                    strokeLinejoin="round" 
                    strokeWidth={2} 
                    d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" 
                  />
                </svg>
                Job Board ID: {job.job_board_id}
              </div>
              
              <div className="mt-4 pt-4 border-t border-gray-200">
                <button className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 transition-colors">
                  Apply Now
                </button>
              </div>
            </div>
          ))}
        </div>
        
        {loaderData?.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">No job posts available</p>
          </div>
        )}
      </div>
    </div>
  );
}