import * as React from "react";
import * as ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import App from "./App";
import { FocusStyleManager } from "@blueprintjs/core";
import HomePage from "./HomePage";
import CheckerDetailPage from "./CheckerDetailPage";
import JobDetailPage from "./JobDetailPage";
import CheckerLayout from "./CheckerLayout";

FocusStyleManager.onlyShowFocusOnTabs();

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      { index: true, element: <HomePage /> },
      {
        path: "checker",
        element: <CheckerLayout />,
        children: [
          {
            path: ":checkerName/job/:jobId",
            element: <JobDetailPage />,
          },
          {
            path: ":checkerName",
            element: <CheckerDetailPage />,
            index: true,
          },
        ],
      },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
