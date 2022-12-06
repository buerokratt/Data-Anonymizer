import { destroy, flow, types } from "mobx-state-tree";
import { Modal } from "../components/Common/Modal/Modal";
import { FF_DEV_2887, isFF } from "../utils/feature-flags";
import { History } from "../utils/history";
import { isDefined } from "../utils/utils";
import { Action } from "./Action";
import * as DataStores from "./DataStores";
import { DynamicModel, registerModel } from "./DynamicModel";
import { TabStore } from "./Tabs";
import { CustomJSON } from "./types";
import { User } from "./Users";

export const AppStore = types
  .model("AppStore", {
    mode: types.optional(
      types.enumeration(["explorer", "labelstream", "labeling"]),
      "explorer",
    ),

    viewsStore: types.optional(TabStore, {
      views: [],
    }),

    project: types.optional(CustomJSON, {}),

    loading: types.optional(types.boolean, false),

    loadingData: false,

    users: types.optional(types.array(User), []),

    taskStore: types.optional(
      types.late(() => {
        return DynamicModel.get("tasksStore");
      }),
      {},
    ),

    annotationStore: types.optional(
      types.late(() => {
        return DynamicModel.get("annotationsStore");
      }),
      {},
    ),

    availableActions: types.optional(types.array(Action), []),

    serverError: types.map(CustomJSON),

    crashed: false,

    interfaces: types.map(types.boolean),

    toolbar: types.string,
  })
  .views((self) => ({
    /** @returns {import("../sdk/dm-sdk").DataManager} */
    get SDK() {
      return self._sdk;
    },

    /** @returns {import("../sdk/lsf-sdk").LSFWrapper} */
    get LSF() {
      return self.SDK.lsf;
    },

    /** @returns {import("../utils/api-proxy").APIProxy} */
    get API() {
      return self.SDK.api;
    },

    get apiVersion() {
      return self.SDK.apiVersion;
    },

    get isLabeling() {
      return (
        !!self.dataStore?.selected ||
        self.isLabelStreamMode ||
        self.mode === "labeling"
      );
    },

    get isLabelStreamMode() {
      return self.mode === "labelstream";
    },

    get isExplorerMode() {
      return self.mode === "explorer" || self.mode === "labeling";
    },

    get currentView() {
      return self.viewsStore.selected;
    },

    get dataStore() {
      switch (self.target) {
        case "tasks":
          return self.taskStore;
        case "annotations":
          return self.annotationStore;
        default:
          return null;
      }
    },

    get target() {
      return self.viewsStore.selected?.target ?? "tasks";
    },

    get labelingIsConfigured() {
      return self.project?.config_has_control_tags === true;
    },

    get labelingConfig() {
      return self.project.label_config_line ?? self.project.label_config;
    },

    get showPreviews() {
      return self.SDK.showPreviews;
    },

    get currentSelection() {
      return self.currentView.selected.snapshot;
    },

    get currentFilter() {
      return self.currentView.filterSnposhot;
    },
  }))
  .volatile(() => ({
    needsDataFetch: false,
    projectFetch: false,
  }))
  .actions((self) => ({
    startPolling() {
      if (self._poll) return;
      if (self.SDK.polling === false) return;

      const poll = async (self) => {
        await self.fetchProject({ interaction: "timer" });
        self._poll = setTimeout(() => poll(self), 10000);
      };

      poll(self);
    },

    beforeDestroy() {
      clearTimeout(self._poll);
      window.removeEventListener("popstate", self.handlePopState);
    },

    setMode(mode) {
      self.mode = mode;
    },

    addActions(...actions) {
      self.availableActions.push(...actions);
    },

    removeAction(id) {
      const action = self.availableActions.find((action) => action.id === id);

      if (action) destroy(action);
    },

    interfaceEnabled(name) {
      return self.interfaces.get(name) === true;
    },

    enableInterface(name) {
      if (!self.interfaces.has(name)) {
        console.warn(`Unknown interface ${name}`);
      } else {
        self.interfaces.set(name, true);
      }
    },

    disableInterface(name) {
      if (!self.interfaces.has(name)) {
        console.warn(`Unknown interface ${name}`);
      } else {
        self.interfaces.set(name, false);
      }
    },

    setToolbar(toolbarString) {
      self.toolbar = toolbarString;
    },

    setTask: flow(function* ({ taskID, annotationID, pushState }) {
      if (pushState !== false) {
        History.navigate({ task: taskID, annotation: annotationID ?? null });
      }

      if (!isDefined(taskID)) return;

      self.loadingData = true;

      if (self.mode === "labelstream") {
        yield self.taskStore.loadNextTask({
          select: !!taskID && !!annotationID,
        });
      }

      if (annotationID !== undefined) {
        self.annotationStore.setSelected(annotationID);
      } else {
        self.taskStore.setSelected(taskID);

        yield self.taskStore.loadTask(taskID, {
          select: !!taskID && !!annotationID,
        });

        const annotation = self.LSF?.currentAnnotation;
        const id = annotation?.pk ?? annotation?.id;

        self.LSF?.setLSFTask(self.taskStore.selected, id);

        self.loadingData = false;
      }
    }),

    unsetTask(options) {
      try {
        self.annotationStore.unset();
        self.taskStore.unset();
      } catch (e) {
        /* Something weird */
      }

      if (options?.pushState !== false) {
        History.navigate({ task: null, annotation: null });
      }
    },

    unsetSelection() {
      self.annotationStore.unset({ withHightlight: true });
      self.taskStore.unset({ withHightlight: true });
    },

    createDataStores() {
      const grouppedColumns = self.viewsStore.columns.reduce((res, column) => {
        res.set(column.target, res.get(column.target) ?? []);
        res.get(column.target).push(column);
        return res;
      }, new Map());

      grouppedColumns.forEach((columns, target) => {
        const dataStore = DataStores[target].create?.(columns);

        if (dataStore) registerModel(`${target}Store`, dataStore);
      });
    },

    startLabelStream(options = {}) {
      if (!self.confirmLabelingConfigured()) return;

      const nextAction = () => {
        self.SDK.setMode("labelstream");

        if (options?.pushState !== false) {
          History.navigate({ labeling: 1 });
        }
      };

      if (
        isFF(FF_DEV_2887) &&
        self.LSF?.lsf?.annotationStore?.selected?.commentStore?.hasUnsaved
      ) {
        Modal.confirm({
          title: "You have unsaved changes",
          body:
            "There are comments which are not persisted. Please submit the annotation. Continuing will discard these comments.",
          onOk() {
            nextAction();
          },
          okText: "Discard and continue",
        });
        return;
      }

      nextAction();
    },

    startLabeling(item, options = {}) {
      if (!self.confirmLabelingConfigured()) return;

      if (self.dataStore.loadingItem) return;

      const nextAction = () => {
        self.SDK.setMode("labeling");

        if (item && !item.isSelected) {
          const labelingParams = {
            pushState: options?.pushState,
          };

          if (isDefined(item.task_id)) {
            Object.assign(labelingParams, {
              annotationID: item.id,
              taskID: item.task_id,
            });
          } else {
            Object.assign(labelingParams, {
              taskID: item.id,
            });
          }

          self.setTask(labelingParams);
        } else {
          self.closeLabeling();
        }
      };

      if (
        isFF(FF_DEV_2887) &&
        self.LSF?.lsf?.annotationStore?.selected?.commentStore?.hasUnsaved
      ) {
        Modal.confirm({
          title: "You have unsaved changes",
          body:
            "There are comments which are not persisted. Please submit the annotation. Continuing will discard these comments.",
          onOk() {
            nextAction();
          },
          okText: "Discard and continue",
        });
        return;
      }

      nextAction();
    },

    confirmLabelingConfigured() {
      if (!self.labelingIsConfigured) {
        Modal.confirm({
          title: "You're almost there!",
          body:
            "Before you can annotate the data, set up labeling configuration",
          onOk() {
            self.SDK.invoke("settingsClicked");
          },
          okText: "Go to setup",
        });
        return false;
      } else {
        return true;
      }
    },

    closeLabeling(options) {
      const { SDK } = self;

      self.unsetTask(options);

      let viewId;
      const tabFromURL = History.getParams().tab;

      if (isDefined(self.currentView)) {
        viewId = self.currentView.tabKey;
      } else if (isDefined(tabFromURL)) {
        viewId = tabFromURL;
      } else if (isDefined(self.viewsStore)) {
        viewId = self.viewsStore.views[0]?.tabKey;
      }

      if (isDefined(viewId)) {
        History.forceNavigate({ tab: viewId });
      }

      SDK.setMode("explorer");
      SDK.destroyLSF();
    },

    handlePopState: (({ state }) => {
      const { tab, task, annotation, labeling } = state ?? {};

      if (tab) {
        const tabId = parseInt(tab);

        self.viewsStore.setSelected(Number.isNaN(tabId) ? tab : tabId, {
          pushState: false,
          createDefault: false,
        });
      }

      if (task) {
        const params = {};

        if (annotation) {
          params.task_id = parseInt(task);
          params.id = parseInt(annotation);
        } else {
          params.id = parseInt(task);
        }

        self.startLabeling(params, { pushState: false });
      } else if (labeling) {
        self.startLabelStream({ pushState: false });
      } else {
        self.closeLabeling({ pushState: false });
      }
    }).bind(self),

    resolveURLParams() {
      window.addEventListener("popstate", self.handlePopState);
    },

    setLoading(value) {
      self.loading = value;
    },

    fetchProject: flow(function* (options = {}) {
      self.projectFetch = options.force === true;

      const oldProject = JSON.stringify(self.project ?? {});
      // const params =
      //   options && options.interaction
      //     ? {
      //       interaction: options.interaction,
      //     }
      //     : null;

      try {
        const newProject = JSON.parse(
          '{"id":23,"title":"Bürokratt_ühestamine","description":"","label_config":"<View>\\n  <View>\\n      <Text name=\\"text\\" value=\\"$text\\"/>\\n  <Labels name=\\"label\\" toName=\\"text\\">\\n    <Label value=\\"PER\\" background=\\"red\\"/>\\n    <Label value=\\"GPE\\" background=\\"darkorange\\"/>\\n    <Label value=\\"LOC\\" background=\\"yellow\\"/>\\n    <Label value=\\"ORG\\" background=\\"green\\"/>\\n    <Label value=\\"PROD\\" background=\\"blue\\"/>\\n    <Label value=\\"EVENT\\" background=\\"brown\\"/>\\n    <Label value=\\"DATE\\" background=\\"black\\"/>\\n    <Label value=\\"TIME\\" background=\\"purple\\"/>\\n    <Label value=\\"TITLE\\" background=\\"cyan\\"/>\\n    <Label value=\\"MONEY\\" background=\\"grey\\"/>\\n    <Label value=\\"PERCENT\\" background=\\"pink\\"/>\\n    <Label value=\\"DOC_ORG\\" background=\\"lightblue\\"/>\\n    <Label value=\\"CARD\\" background=\\"lightgreen\\"/>\\n    <Label value=\\"IBAN\\" background=\\"darkgreen\\"/>\\n    <Label value=\\"DOC_PER\\" background=\\"silver\\"/>\\n    <Label value=\\"IDCODE\\" background=\\"gold\\"/>\\n    <Label value=\\"EMAIL\\" background=\\"purple\\"/>\\n    <Label value=\\"TEL\\" background=\\"black\\"/>\\n  </Labels>\\n  </View>\\n\\n\\n  <View style=\\"box-shadow: 2px 2px 5px #999;                padding: 20px; margin-top: 2em;                border-radius: 5px;\\">\\n  <Header>Juhised</Header>\\n  <Text name=\\"instructions\\">\\n    PER - person names\\nGPE - geopolitical entities\\nLOC - geographical locations\\nORG - organizations\\nPROD - products, things, works of art\\nEVENT - events\\nDATE - dates\\nTIME - times, konkreetne aeg nt “kell 12:00”. Umbmäärased ajad nagu “õhtul”, “hilja” siia alla ei käi.\\nTITLE - titles and professions. Konkreetsed tiitlid, nt “president”, “peaminister”, “härra”, “riigikogu liige”. Umbmäärased tiitlid “liige” siia alla ei käi. Elukutsetega samuti, konkreetsed elukutsed.\\nMONEY - monetary expressions\\nPERCENT - percentages\\nDOC_ORG - id of organisation document\\nCARD - banking or similar card number\\nIBAN - IBAN account number\\nDOC_PER - Personal document number\\nIDCODE - personal ID code\\nEMAIL - email address\\nTEL - phone number\\n\\n  </Text>\\n  </View>  \\n</View>","expert_instruction":"Peamiseks ülesandeks on täiendavalt tekstist märkida olemid (Nimi, asutus, jne), mis vastavad välja toodud olemitüüpidele. Kui midagi ei ole vaja märgnedada täiendavalt , siis pange taskile \\"Submit\\". Märkimiseks kõigepealt valida olemitüüp ja seejärel valida tekstiosa, mis sellele olemile vastab. Ühe olemitüübi valikuga märkida täpselt üks olem. (Nt kui on kaks eraldi aadressi, siis tuleb kaks korda olemitüüpi valida, mõlema jaoks eraldi.)","show_instruction":true,"show_skip_button":true,"enable_empty_annotation":true,"show_annotation_history":false,"organization":1,"color":"#FFFFFF","maximum_annotations":1,"is_published":false,"model_version":"undefined","is_draft":false,"created_by":{"id":9,"first_name":"","last_name":"","email":"sander.tars@mindtitan.com","avatar":null},"created_at":"2022-09-28T13:14:50.667092Z","min_annotations_to_start_training":0,"start_training_on_annotation_update":false,"show_collab_predictions":true,"num_tasks_with_annotations":null,"task_number":null,"useful_annotation_number":null,"ground_truth_number":null,"skipped_annotations_number":null,"total_annotations_number":null,"total_predictions_number":null,"sampling":"Sequential sampling","show_ground_truth_first":false,"show_overlap_first":false,"overlap_cohort_percentage":100,"task_data_login":null,"task_data_password":null,"control_weights":{"label":{"type":"Labels","labels":{"GPE":1,"LOC":1,"ORG":1,"PER":1,"TEL":1,"CARD":1,"DATE":1,"IBAN":1,"PROD":1,"TIME":1,"EMAIL":1,"EVENT":1,"MONEY":1,"TITLE":1,"IDCODE":1,"DOC_ORG":1,"DOC_PER":1,"PERCENT":1},"overall":1}},"parsed_label_config":{"label":{"type":"Labels","to_name":["text"],"inputs":[{"type":"Text","value":"text"}],"labels":["PER","GPE","LOC","ORG","PROD","EVENT","DATE","TIME","TITLE","MONEY","PERCENT","DOC_ORG","CARD","IBAN","DOC_PER","IDCODE","EMAIL","TEL"],"labels_attrs":{"PER":{"value":"PER","background":"red"},"GPE":{"value":"GPE","background":"darkorange"},"LOC":{"value":"LOC","background":"yellow"},"ORG":{"value":"ORG","background":"green"},"PROD":{"value":"PROD","background":"blue"},"EVENT":{"value":"EVENT","background":"brown"},"DATE":{"value":"DATE","background":"black"},"TIME":{"value":"TIME","background":"purple"},"TITLE":{"value":"TITLE","background":"cyan"},"MONEY":{"value":"MONEY","background":"grey"},"PERCENT":{"value":"PERCENT","background":"pink"},"DOC_ORG":{"value":"DOC_ORG","background":"lightblue"},"CARD":{"value":"CARD","background":"lightgreen"},"IBAN":{"value":"IBAN","background":"darkgreen"},"DOC_PER":{"value":"DOC_PER","background":"silver"},"IDCODE":{"value":"IDCODE","background":"gold"},"EMAIL":{"value":"EMAIL","background":"purple"},"TEL":{"value":"TEL","background":"black"}}}},"evaluate_predictions_automatically":false,"config_has_control_tags":true,"skip_queue":"REQUEUE_FOR_OTHERS","reveal_preannotations_interactively":false,"can_delete_tasks":true,"can_manage_annotations":true,"can_manage_tasks":true,"source_syncing":false,"target_syncing":false,"task_count":8773,"annotation_count":8749}',
        );
        const entities = yield self.apiCall("entity");

        const entity_string = entities.reduce(
          (total, curr) => total + `<Label value="${curr["name"]}"/> \n`,
          "",
        );

        newProject["label_config"] = `<View>
        <View>
            <Text name="text" value="$text"/>
        <Labels name="label" toName="text">
        ${entity_string}
        </Labels>
        </View>
      </View>`;
        const projectLength = Object.entries(self.project ?? {}).length;

        self.needsDataFetch =
          options.force !== true && projectLength > 0
            ? self.project.task_count !== newProject.task_count ||
              self.project.task_number !== newProject.task_number ||
              self.project.annotation_count !== newProject.annotation_count ||
              self.project.num_tasks_with_annotations !==
                newProject.num_tasks_with_annotations
            : false;

        if (JSON.stringify(newProject ?? {}) !== oldProject) {
          self.project = newProject;
        }
      } catch {
        self.crash();
        return false;
      }
      self.projectFetch = false;
      return true;
    }),

    fetchActions() {
      // const serverActions = yield self.apiCall("actions");
      const serverActions = [];

      self.addActions(...(serverActions ?? []));
    },

    fetchUsers() {
      // const list = yield self.apiCall("users");
      const list = [];

      self.users.push(...list);
    },

    fetchData: flow(function* ({ isLabelStream } = {}) {
      self.setLoading(true);

      const { tab, task, labeling, query } = History.getParams();

      self.viewsStore.fetchColumns();

      const requests = [self.fetchProject(), self.fetchUsers()];

      if (!isLabelStream) {
        requests.push(self.fetchActions());

        if (self.SDK.settings?.onlyVirtualTabs) {
          requests.push(
            self.viewsStore.addView(
              { virtual: true, tab },
              { autosave: false, reload: false },
            ),
          );
        } else {
          requests.push(self.viewsStore.fetchTabs(tab, task, labeling));
        }
      } else if (isLabelStream && !!tab) {
        const { selectedItems } = JSON.parse(decodeURIComponent(query ?? "{}"));

        requests.push(self.viewsStore.fetchSingleTab(tab, selectedItems ?? {}));
      }

      const [projectFetched] = yield Promise.all(requests);

      if (projectFetched) {
        self.resolveURLParams();

        self.setLoading(false);

        self.startPolling();
      }
    }),

    apiCall: flow(function* (methodName, params, body) {
      const apiTransform = self.SDK.apiTransform?.[methodName];
      const requestParams = apiTransform?.params?.(params) ?? params ?? {};
      const requestBody = apiTransform?.body?.(body) ?? body ?? undefined;

      let result = yield self.API[methodName](requestParams, requestBody);

      if (result.error && result.status !== 404) {
        if (result.response) {
          self.serverError.set(methodName, {
            error: "Something went wrong",
            response: result.response,
          });
        }

        console.warn({
          message: "Error occurred when loading data",
          description: result?.response?.detail ?? result.error,
        });

        self.SDK.invoke("error", result);

        // notification.error({
        //   message: "Error occurred when loading data",
        //   description: result?.response?.detail ?? result.error,
        // });
      } else {
        self.serverError.delete(methodName);
      }

      return result.response;
    }),

    invokeAction: flow(function* (actionId, options = {}) {
      const view = self.currentView ?? {};

      const needsLock =
        self.availableActions.findIndex((a) => a.id === actionId) >= 0;

      const { selected } = view;
      const actionCallback = self.SDK.getAction(actionId);

      if (view && needsLock && !actionCallback) view.lock();

      const labelStreamMode = localStorage.getItem("dm:labelstream:mode");

      // @todo this is dirty way to sync across nested apps
      // don't apply filters for "all" on "next_task"
      const actionParams = {
        ordering: view.ordering,
        selectedItems: selected?.snapshot ?? { all: false, included: [] },
        filters: {
          conjunction: view.conjunction ?? "and",
          items: view.serializedFilters ?? [],
        },
      };

      if (actionId === "next_task") {
        if (labelStreamMode === "all") {
          delete actionParams.filters;

          if (
            actionParams.selectedItems.all === false &&
            actionParams.selectedItems.included.length === 0
          ) {
            delete actionParams.selectedItems;
            delete actionParams.ordering;
          }
        } else if (labelStreamMode === "filtered") {
          delete actionParams.selectedItems;
        }
      }

      if (actionCallback instanceof Function) {
        return actionCallback(actionParams, view);
      }

      const requestParams = {
        id: actionId,
      };

      if (isDefined(view.id) && !view?.virtual) {
        requestParams.tabID = view.id;
      }

      if (options.body) {
        Object.assign(actionParams, options.body);
      }

      const result = yield self.apiCall("invokeAction", requestParams, {
        body: actionParams,
      });

      if (result.reload) {
        self.SDK.reload();
        return;
      }

      if (options.reload !== false) {
        yield view.reload();
        self.fetchProject();
        view.clearSelection();
      }

      view?.unlock?.();

      return result;
    }),

    crash() {
      self.destroy();
      self.crashed = true;
      self.SDK.invoke("crash");
    },

    destroy() {
      if (self.taskStore) {
        self.taskStore?.clear();
        self.taskStore = undefined;
      }

      if (self.annotationStore) {
        self.annotationStore?.clear();
        self.annotationStore = undefined;
      }

      clearTimeout(self._poll);
    },
  }));
