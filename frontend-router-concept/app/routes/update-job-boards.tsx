import { Form, Link, useFetcher, useLoaderData } from "react-router";
import type { Route } from "../+types/root";
import { Field, FieldGroup, FieldLabel, FieldLegend } from "~/components/ui/field";
import { Input } from "~/components/ui/input";
import { Button } from "~/components/ui/button";
import jobBoards from "./job-boards";

// get data based on the job id
export async function clientLoader({ params }: Route.LoaderArgs) {
  const res = await fetch(`/api/job-boards/${params.jobBoardId}`);
  const jobBoards = await res.json();
  return { jobBoards };
}

//submition of the data
export async function clientAction({request}: Route.ClientActionArgs){
  const formData = await request.formData()
  const job_board_id = formData.get('job_board_id')
  await fetch(`/api/job-boards/${job_board_id}/update`, {
    method: 'PUT',
  })
}

export default async function UpdateJobBoards(_: Route.ComponentProps){

    return (
        <div className="w-full max-w-md">
      <Form method="post" encType="multipart/form-data">
        <FieldGroup>
          <FieldLegend>Update Job Board</FieldLegend>
          <Field>
            <FieldLabel htmlFor="slug">
              Slug
            </FieldLabel>
            <Input
              id="slug"
              name="slug"
              placeholder="acme"
              required
            />
          </Field>
          <Field>
            <FieldLabel htmlFor="logo">
              Logo
            </FieldLabel>
            <Input
              id="logo"
              name="logo"
              type="file"
              required
            />
          </Field>
          <div className="float-right">
            <Field orientation="horizontal">
              <Button type="submit">Submit</Button>
              <Button variant="outline" type="button">
                <Link to="/job-boards">Cancel</Link>
              </Button>
            </Field>
          </div>
          <input type="hidden" name="id" value={jobBoards.id} />
        </FieldGroup>
      </Form>
    </div>
    )
}