import { flow, getRoot, types } from "mobx-state-tree";
import { guidGenerator } from "../../utils/random";
import { isDefined } from "../../utils/utils";
import {
  DEFAULT_PAGE_SIZE,
  getStoredPageSize
} from "../../components/Common/Pagination/Pagination";
import { FF_DEV_1470, isFF } from "../../utils/feature-flags";

const listIncludes = (list, id) => {
  const index =
    id !== undefined
      ? Array.from(list).findIndex((item) => item.id === id)
      : -1;

  return index >= 0;
};

const fieldMappingDict = {
  'data.text': `Corpora_Tasks."raw_text"`,
  'id': `Corpora_Tasks."id"`,
  'completed_at': `Corpora_Tasks."created_at"`,
};

const getClauseForSortCondition = (ordering) => {
  const field = fieldMappingDict[ordering[0]?.split(':')?.slice(-1)[0]];
  const ascend = ordering[0][0] !== '-';

  return `${field} ${ascend ? 'ASC' : 'DESC'}`;
};

const getClauseForWhereCondition = (filter) => {
  const field = fieldMappingDict[filter?.filter?.split(':')?.slice(-1)[0]];
  let fieldValue = filter.value;
  const operator = filter.operator;
  const fieldType = filter.type;

  if (fieldType === 'Datetime' && operator !== 'empty') {
    if (operator === 'in' || operator === 'not_in') {
      fieldValue = {
        max: `timestamp '${fieldValue.max}'`,
        min: `timestamp '${fieldValue.min}'`,
      };
    }
    else fieldValue = `timestamp '${fieldValue}'`;
  }
  
  if (operator === 'equal') return `${field} = ${fieldType === 'Number' ? fieldValue : `'${fieldValue}'`}`;
  else if (operator === 'not_equal') return `${field} <> ${fieldType === 'Number' ? fieldValue : `'${fieldValue}'`}`;
  else if (operator === 'less') return `${field} < ${fieldValue}`;
  else if (operator === 'greater') return `${field} > ${fieldValue}`;
  else if (operator === 'less_or_equal') return `${field} <= ${fieldValue}`;
  else if (operator === 'greater_or_equal') return `${field} >= ${fieldValue}`;
  else if (operator === 'in') return `(${field} >= ${fieldValue.min} AND ${field} <= ${fieldValue.max})`;
  else if (operator === 'not_in') return `NOT (${field} >= ${fieldValue.min} AND ${field} <= ${fieldValue.max})`;
  else if (operator === 'empty') return [1, 'true', true].includes(fieldValue) ? fieldType === 'String' ? `(${field} = '' OR ${field} IS NULL)` : `${field} IS NULL` : fieldType === 'String' ? `(${field} <> '' AND ${field} IS NOT NULL)` : `${field} IS NOT NULL`;
  else if (operator === 'contains') return `${field} LIKE '%${fieldValue}%'`;
  else if (operator === 'not_contains') return `${field} NOT LIKE '%${fieldValue}%'`;
  else if (operator === 'regex') return `${field} ~ '${fieldValue}'`;
};

const MixinBase = types
  .model("InfiniteListMixin", {
    page: types.optional(types.integer, 0),
    pageSize: types.optional(
      types.integer,
      getStoredPageSize("tasks", DEFAULT_PAGE_SIZE),
    ),
    total: types.optional(types.integer, 0),
    loading: false,
    loadingItem: false,
    loadingItems: types.optional(types.array(types.number), []),
    updated: guidGenerator(),
  })
  .views((self) => ({
    get API() {
      return self.root.API;
    },

    get root() {
      return getRoot(self);
    },

    get totalPages() {
      return Math.ceil(self.total / self.pageSize);
    },

    get hasNextPage() {
      return self.page !== self.totalPages;
    },

    get isLoading() {
      return self.loadingItem || self.loadingItems.length > 0;
    },

    get length() {
      return self.list.length;
    },

    itemIsLoading(id) {
      return self.loadingItems.includes(id);
    },
  }))
  .actions((self) => ({
    setSelected(val) {
      let selected;

      if (typeof val === "number") {
        selected = self.list.find((t) => t.id === val);
      } else {
        selected = val;
      }

      if (selected && selected.id !== self.selected?.id) {
        self.selected = selected;
        self.highlighted = selected;

        getRoot(self).SDK.invoke("taskSelected");
      }
    },

    hasRecord(id) {
      return self.list.some((t) => t.id === Number(id));
    },

    unset({ withHightlight = false } = {}) {
      self.selected = undefined;
      if (withHightlight) self.highlighted = undefined;
    },

    setList({ list, total, reload }) {
      const newEntity = list.map((t) => ({
        ...t,
        source: JSON.stringify(t),
      }));

      self.total = total;

      newEntity.forEach((n) => {
        const index = self.list.findIndex((i) => i.id === n.id);

        if (index >= 0) {
          self.list.splice(index, 1);
        }
      });

      if (reload) {
        self.list = [...newEntity];
      } else {
        self.list.push(...newEntity);
      }
    },

    setLoading(id) {
      if (id !== undefined) {
        self.loadingItems.push(id);
      } else {
        self.loadingItem = true;
      }
    },

    finishLoading(id) {
      if (id !== undefined) {
        self.loadingItems = self.loadingItems.filter((item) => item !== id);
      } else {
        self.loadingItem = false;
      }
    },

    clear() {
      self.highlighted = undefined;
      self.list = [];
      self.page = 0;
      self.total = 0;
    },
  }));

export const DataStore = (
  modelName,
  { listItemType, apiMethod, properties },
) => {
  const model = types
    .model(modelName, {
      ...(properties ?? {}),
      list: types.optional(types.array(listItemType), []),
      selectedId: types.optional(types.maybeNull(types.number), null),
      highlightedId: types.optional(types.maybeNull(types.number), null),
    })
    .views((self) => ({
      get selected() {
        return self.list.find(({ id }) => id === self.selectedId);
      },

      get highlighted() {
        return self.list.find(({ id }) => id === self.highlightedId);
      },

      set selected(item) {
        self.selectedId = item?.id ?? item;
      },

      set highlighted(item) {
        self.highlightedId = item?.id ?? item;
      },
    }))
    .volatile(() => ({
      requestId: null,
    }))
    .actions((self) => ({
      updateItem(itemID, patch) {
        let item = self.list.find((t) => t.id === itemID);

        if (item) {
          item.update(patch);
        } else {
          item = listItemType.create(patch);
          self.list.push(item);
        }

        return item;
      },

      fetch: flow(function* ({
        id,
        query,
        pageNumber = null,
        reload = false,
        interaction,
        pageSize,
      } = {}) {
        const currentView = getRoot(self).viewsStore.selected;
        let interactionParams = currentView.snapshot;

        let currentViewId, currentViewQuery;
        const requestId = (self.requestId = guidGenerator());

        if (id) {
          currentViewId = id;
          currentViewQuery = query;
        } else {
          currentViewId = currentView?.id;
          currentViewQuery = currentView?.virtual ? currentView?.query : null;
        }

        if (!isDefined(currentViewId)) return;

        self.loading = true;

        if (
          interaction === "filter" ||
          (!isFF(FF_DEV_1470) && interaction === "ordering") ||
          (!isFF(FF_DEV_1470) && reload)
        ) {
          self.page = 1;
        } else if (reload || isDefined(pageNumber)) {
          if (self.page === 0) self.page = 1;
          else if (isDefined(pageNumber)) self.page = pageNumber;
        } else {
          self.page++;
        }

        if (pageSize) {
          self.pageSize = pageSize;
        } else {
          self.pageSize = getStoredPageSize("tasks", DEFAULT_PAGE_SIZE);
        }
        let whereCondition = `corpora_id = '${interactionParams.project}'`;
        let sortCondition = `Corpora_Tasks."id" DESC`;

        if (interactionParams?.data?.filters?.items?.length > 0) {
          whereCondition = interactionParams?.data?.filters?.items.reduce((acc, curr, index) => {
            const clause = getClauseForWhereCondition(curr);

            if (index !== 0) acc += ` ${interactionParams?.data?.filters?.conjunction?.toUpperCase()} `;
            return acc + clause;
          } , `${whereCondition} AND `);
        }
        
        if (interactionParams?.data?.ordering?.length) {
          sortCondition = getClauseForSortCondition(interactionParams?.data?.ordering);
        }
        
        const params = {
          page: self.page,
          page_size: self.pageSize,
          where_condition: whereCondition,
          sort_condition: sortCondition,
        };

        if (currentViewQuery) {
          params.query = currentViewQuery;
        } else {
          params.view = currentViewId;
        }

        if (interaction) Object.assign(params, { interaction });
        let data = yield getRoot(self).apiCall(apiMethod, params);

        if (apiMethod === "tasks") {
          let result = {
            total: data?.[0]?.fullCount,
            total_annotations: 0,
            total_predictions: 0,
            tasks: [],
          };

          for (let task of data) {
            result["tasks"].push({
              cancelled_annotations: 0,
              completed_at: task["createdAt"],
              annotations_results: "",
              data: {
                text: task["rawText"],
              },
              id: task["id"],
              predictions_results: "",
              total_annotations: 0,
              total_predictions: task["predictions"] ? 1 : 0,
              annotations_ids: "",
              drafts: [],
              file_upload: null,
              predictions_model_versions: "",
            });
          }
          data = result;
        }
        // We cancel current request processing if request id
        // cnhaged during the request. It indicates that something
        // triggered another request while current one is not yet finished
        if (requestId !== self.requestId) {
          console.log(`Request ${requestId} was cancelled by another request`);
          return;
        }

        const highlightedID = self.highlighted;

        const { total, [apiMethod]: list } = data;

        if (list)
          self.setList({
            total,
            list,
            reload: reload || isDefined(pageNumber),
          });

        if (
          isDefined(highlightedID) &&
          !listIncludes(self.list, highlightedID)
        ) {
          self.highlighted = null;
        }

        self.postProcessData?.(data);

        self.loading = false;

        getRoot(self).SDK.invoke("dataFetched", self);
      }),

      reload: flow(function* ({ id, query, interaction } = {}) {
        yield self.fetch({ id, query, reload: true, interaction });
      }),

      focusPrev() {
        const index = Math.max(0, self.list.indexOf(self.highlighted) - 1);

        self.highlighted = self.list[index];
        self.updated = guidGenerator();
      },

      focusNext() {
        const index = Math.min(
          self.list.length - 1,
          self.list.indexOf(self.highlighted) + 1,
        );

        self.highlighted = self.list[index];
        self.updated = guidGenerator();
      },
    }));

  return types.compose(MixinBase, model);
};
