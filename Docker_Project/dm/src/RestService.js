const API_URL = process.env.REACT_APP_API_URL;

const listRegex = async () => {
  try {
    let response = await fetch(`${API_URL}/regex`);
    response = await response.json();
    return response.response;
  } catch (err) {
    console.log(err);
  }
};

const getCorporaInfo = async () => {
  try {
    let response = await fetch(`${API_URL}/corpora_info`);
    response = await response.json();
    return response.response;
  } catch (err) {
    console.log(err);
  }
};

const getTrainedCorporaInfo = async () => {
  try {
    let response = await fetch(`${API_URL}/trained_corpora_info`);
    response = await response.json();
    return response.response;
  } catch (err) {
    console.log(err);
  }
};

const deleteRegex = async (id) => {
  try {
    let response = await fetch(`${API_URL}/delete_regex?id=${id}`);
    response = await response.json();
    return response.response;
  } catch (err) {
    console.log(err);
  }
};

const deleteCorporaInfo = async (id) => {
  try {
    let response = await fetch(`${API_URL}/delete_corpora_info?id=${id}`);
    response = await response.json();
    return response.response;
  } catch (err) {
    console.log(err);
  }
};

const getEntities = async () => {
  try {
    let response = await fetch(`${API_URL}/entity`);
    response = await response.json();
    return response.response;
  } catch (err) {
    console.log(err);
  }
};

const fetchTrainingStatus = async () => {
  try {
    let response = await fetch(`${API_URL}/training_status`);
    response = await response.json();
    return response.response;
  } catch (err) {
    console.log(err);
  }
};

const addCorporaInfo = async (fileName, fileSize) => {
  try {
    let response = await fetch(`${API_URL}/corpora_info`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        source_file_name: fileName,
        source_file_size: fileSize,
      }),
    });
    response = await response.json();
    return response.response;
  } catch (err) {
    console.log(err);
  }
};

const uploadCorpus = async (payload) => {
  try {
    let response = await fetch(`${API_URL}/corpora`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
    response = await response.json();
    return response.response;
  } catch (err) {
    console.log(err);
  }
};

const startTraining = async () => {
  try {
    let response = await fetch(`${API_URL}/train`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    });
    response = await response.json();
    return response.response;
  } catch (err) {
    console.log(err);
  }
};

const annotateCorpora = async () => {
  try {
    let response = await fetch(`${API_URL}/annotate_corpora`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    });
    response = await response.json();
    return response.response;
  } catch (err) {
    console.log(err);
  }
};

const fetchPreLabellingStatus = async (taskId) => {
  try {
    let response = await fetch(
      `${API_URL}/prelabelling_status?taskId=${taskId}`
    );
    response = await response.json();
    return response.response;
  } catch (err) {
    console.log(err);
  }
};

const createRegex = async (regex, entity) => {
  try {
    let response = await fetch(`${API_URL}/regex`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ regex, entity }),
    });
    response = await response.json();
    return response.response;
  } catch (err) {
    console.log(err);
  }
};

const createEntity = async (name, description) => {
  try {
    let response = await fetch(`${API_URL}/entity`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name, description }),
    });
    response = await response.json();
    return response.response;
  } catch (err) {
    console.log(err);
  }
};

const pseudonymiseText = async (text) => {
  try {
    let response = await fetch(`${API_URL}/pseudonymise`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        texts: [text],
        tokenize: true,
        truecase: true,
        pseudonymise: true,
        thresholds: {},
      }),
    });
    response = await response.json();
    return response.response;
  } catch (err) {
    console.log(err);
  }
};

export {
  getEntities,
  pseudonymiseText,
  listRegex,
  fetchTrainingStatus,
  uploadCorpus,
  startTraining,
  annotateCorpora,
  deleteRegex,
  createRegex,
  createEntity,
  fetchPreLabellingStatus,
  getCorporaInfo,
  addCorporaInfo,
  getTrainedCorporaInfo,
  deleteCorporaInfo,
};
