let axios = require("axios");
let fs = require("fs");
let base64 = require("base-64");

let token = process.env.GIT_TOKEN;
let url = process.env.API_URL || "http://127.0.0.1:8080";
let GIT_OWNER = process.env.GIT_OWNER;
let GIT_REPO = process.env.GIT_REPO;

downloadCorpusAndUploadToGit();

async function downloadCorpusAndUploadToGit() {
  try {
    let page = 1;
    let result = [];
    let responseProject = await axios.get(`${url}/project`);
    let corporaId = responseProject.data.response[0].corporaId;
    while (true) {
      let response = await axios.get(`${url}/tasks`, {
        params: {
          page: `${page}`,
          page_size: "100",
          where_condition: `corpora_id = '${corporaId}'`,
          sort_condition: `Corpora_Tasks."id" DESC`,
        },
      });
      let responseBody = response.data.response;
      let total = responseBody[0] && responseBody[0].fullCount;
      result = result.concat(
        responseBody.map((x) => ({
          predictions: [{ result: JSON.parse(x.predictions || "[]") }],
          data: {
            text: x.rawText,
          },
        }))
      );
      if (!total || result.length >= total) break;
      page++;
    }
    uploadFileApi(
      token,
      base64.encode(JSON.stringify(result, null, " ")),
      corporaId
    );
  } catch (err) {
    console.log(err);
  }
}

function uploadFileApi(token, content, corporaId) {
  let shaDict;
  try {
    shaDict = JSON.parse(fs.readFileSync("sha.txt").toString());
  } catch (err) {
    shaDict = {};
  }
  let data = JSON.stringify({
    message: `Corpus commited at ${new Date().toISOString()}`,
    content: `${content}`,
    sha: shaDict[corporaId],
  });

  let config = {
    method: "put",
    url: `https://api.github.com/repos/${GIT_OWNER}/${GIT_REPO}/contents/corpus_${corporaId}.json`,
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    data: data,
  };

  axios(config)
    .then(function (response) {
      shaDict[corporaId] = response.data.content.sha;
      fs.writeFileSync("sha.txt", JSON.stringify(shaDict));
      console.log(JSON.stringify(response.data));
    })
    .catch(function (error) {
      console.log(error);
    });
}
