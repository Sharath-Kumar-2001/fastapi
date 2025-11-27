import { layout, route, type RouteConfig } from "@react-router/dev/routes";

export default [
    layout("layouts/default.tsx",[
        route("job-boards", "routes/job-boards.tsx"), // for each api create each routes
        route("job-boards/:jobBoardId/job-posts", "routes/job-posts.tsx"),
        route("/","routes/home.tsx"),
        route("/job-boards/new", "routes/new-job-board.tsx"),
        route("/job-boards/:jobBoardId/update", "routes/update-job-boards.tsx"),
        route("/admin-login", "route/login.tsx")
    ])
] satisfies RouteConfig;
