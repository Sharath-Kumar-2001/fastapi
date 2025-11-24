import {
  isRouteErrorResponse,
  useLoaderData,
  Link,
  Links,
  Meta,
  Outlet,
  Scripts,
  ScrollRestoration,
} from "react-router";
import type { Route } from "../+types/root";


// api call to fetch the data
export async function clientLoader() {
  const res = await fetch(`/api/job-boards`);
  const jobBoards = await res.json();
  return {jobBoards}
}

// view/ render functions to show data
export default function JobBoards({loaderData}) {
  return (
    <div>
      {loaderData.jobBoards.map(
        (jobBoard) => 
          <p key={jobBoard.id}>
            <Link to={`/job-boards/${jobBoard.id}/job-posts`}>{jobBoard.slug}</Link>
          </p>
      )}
    </div>
    )
}


