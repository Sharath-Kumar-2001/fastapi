import { Link, useFetcher, useLoaderData } from "react-router";
import { Avatar, AvatarImage } from "@radix-ui/react-avatar";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "~/components/ui/table";
import { Button } from "~/components/ui/button";
import type { Route } from "../+types/root";

// Fetch job boards from API
export async function clientLoader() {
  const res = await fetch(`/api/job-boards`);
  const jobBoards = await res.json();
  return { jobBoards };
}

export async function clientAction({ request}: Route.ClientActionArgs) {
  const formData = await request.formData()
  const jobId = formData.get('job_id')
  await fetch(`/api/job-boards/${jobId}/delete`, {
    method: 'DELETE',
  })
}


// Beautiful Job Boards Page
export default function JobBoards() {
  const { jobBoards } = useLoaderData() as { jobBoards: any[] };
  const fetcher = useFetcher();
  return (
    <div className="min-h-screen bg-black text-white relative overflow-hidden">
      {/* Futuristic gradient background - same style as Home */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-900 via-black to-blue-900 -z-10"></div>

      {/* Main content */}
      <div className="relative z-10 min-h-screen flex flex-col items-center justify-center px-6 py-16">

        {/* Title */}
        <div className="text-center mb-16">
          <h1 className="text-5xl md:text-7xl font-extrabold">
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400">
              Choose Your Board
            </span>
          </h1>
          <p className="text-xl text-gray-300 mt-4">Pick a company and explore open roles</p>
          <Button><Link to="/job-boards/new">Add New Job Board</Link></Button>
        </div>
        
        {/* Beautiful centered table */}
        <div className="w-full max-w-4xl">
          
          <div className="backdrop-blur-xl bg-white/5 border border-white/10 rounded-3xl overflow-hidden shadow-2xl">
            <Table>
              <TableHeader>
                <TableRow className="border-b border-white/10">
                  <TableHead className="text-cyan-400 text-lg font-semibold">Logo</TableHead>
                  <TableHead className="text-cyan-400 text-lg font-semibold">Company</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {jobBoards.map((jobBoard) => (
                  <TableRow 
                    key={jobBoard.id} 
                    className="hover:bg-white/10 transition duration-200 border-b border-white/5"
                  >
                    <TableCell className="py-6">
                      {jobBoard.logo_url ? (
                        <Avatar className="w-12 h-12 rounded-full ring-2 ring-cyan-500/50">
                          <AvatarImage src={jobBoard.logo_url} alt={jobBoard.slug} />
                        </Avatar>
                      ) : (
                        <div className="w-12 h-12 bg-gradient-to-br from-cyan-500 to-purple-600 rounded-full flex items-center justify-center text-xl font-bold">
                          {jobBoard.slug[0].toUpperCase()}
                        </div>
                      )}
                    </TableCell>
                    <TableCell className="text-xl">
                      <Link 
                        to={`/job-boards/${jobBoard.id}/job-posts`}
                        className="text-white font-medium capitalize hover:text-cyan-400 transition flex items-center gap-2 group"
                      >
                        {jobBoard.slug.replace(/-/g, " ")}
                        <span className="text-cyan-400 opacity-0 group-hover:opacity-100 transition">→</span>
                      </Link>
                    </TableCell>
                    <TableCell>
                      <fetcher.Form method="put">
                        <input name="job_board_id" type="hidden" value={jobBoard.id}></input>
                        <Button><Link to = {`/job-boards/${jobBoard.id}/update`}>Edit</Link></Button>
                      </fetcher.Form>
                    </TableCell>
                    <TableCell>
                      <fetcher.Form method="post" onSubmit={(event) => {
                      const response = confirm(
                        `Please confirm you want to delete this job board '${jobBoard.slug}'.`,
                      );
                      if (!response) {
                        event.preventDefault();
                      }
                    }}>
                        <input name="job_board_id" type="hidden" value={jobBoard.id}></input>
                        <Button>Delete</Button>
                      </fetcher.Form>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </div>

        {/* Back to home (optional small link) */}
        <div className="mt-12">
          <Link to="/" className="text-gray-400 hover:text-cyan-400 transition text-sm">
            ← Back to Home
          </Link>
        </div>
      </div>
    </div>
  );
}