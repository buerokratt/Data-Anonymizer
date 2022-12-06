// import { Button } from "./components/Common/Button/Button";

const API_GATEWAY = process.env.API_GATEWAY;
const LS_ACCESS_TOKEN = process.env.LS_ACCESS_TOKEN;

/**
 * @param {import("./sdk/dm-sdk").DataManager} DataManager
 */
export const initDevApp = async (DataManager) => {
  const gatewayAPI = API_GATEWAY ?? "http://localhost:8081/api";
  const useExternalSource = !!gatewayAPI;
  let projectResponse = await fetch(`${API_GATEWAY}/project`);

  projectResponse = await projectResponse.json();
  const dm = new DataManager({
    root: document.getElementById("app"),
    projectId: projectResponse?.response?.[0]?.corporaId,
    toolbar:
      "actions columns filters ordering review-button label-button loading-possum error-box | refresh view-toggle",
    apiGateway: gatewayAPI,
    apiVersion: 2,
    apiMockDisabled: useExternalSource,
    apiHeaders: {
      Authorization: `Token ${LS_ACCESS_TOKEN}`,
    },
    interfaces: {
      groundTruth: true,
    },
    labelStudio: {
      user: {
        pk: 1,
        firstName: "James",
        lastName: "Dean",
      },
    },
    table: {
      hiddenColumns: {
        explore: ["tasks:completed_at", "tasks:data"],
      },
      visibleColumns: {
        labeling: [
          "tasks:id",
          "tasks:was_cancelled",
          "tasks:data.image",
          "tasks:data.text",
          "annotations:id",
          "annotations:task_id",
        ],
      },
    },
    instruments: {
      "review-button": () => {
        return () => <div/>;
      },
    },
  });

  dm.on("lsf:groundTruth", () => {
    console.log("lsf ground truth set");
  });

  dm.on("taskSelected", () => {
    console.log("task selected");
  });
};