const chai = require("chai");
const chaiHttp = require("chai-http");
const should = chai.should();
const expect = require("chai").expect;
var fs = require("fs");

const RESQL_URL = process.env.RESQL_URL || "http://resql:8082";
const RUUTER_URL = process.env.RUUTER_URL || "http://ruuter:8080";

chai.use(chaiHttp);
describe("Tests", () => {
  beforeEach(async () => {
    await chai.request(RESQL_URL).post("/create_test_schema");
  });

  it("should create and read a corpora info record", async () => {
    //Fresh DB State should have no data.
    let res = await chai.request(RUUTER_URL).get("/corpora_info");
    res.should.have.status(200);
    res.body.should.have.property("response");
    res.body.response.should.be.a("array").of.length(0);

    let testCases = [
      {
        requestBody: {
          source_file_name: "korpus_test.txt",
          source_file_size: "12312",
        },
      },
      {
        requestBody: {
          source_file_name: "korpus_test_updated.txt",
          source_file_size: "4232",
        },
      },
    ];

    for (let testCase of testCases) {
      // Create new corpora info record
      res = await chai
        .request(RUUTER_URL)
        .post("/corpora_info")
        .send(testCase.requestBody);
      res.should.have.status(200);
      res.body.should.have.property("response");
      res.body.response.should.be.a("array").of.length(1);

      const recordWritten = res.body.response.pop();
      recordWritten.should.have.property("corporaId");
      recordWritten.should.have.property("createdAt");

      // Read latest corpora info record
      res = await chai.request(RUUTER_URL).get("/corpora_info");
      res.should.have.status(200);
      res.body.should.have.property("response");
      res.body.response.should.be.a("array").of.length(1);

      const recordRead = res.body.response.pop();
      recordRead.should.have.property("corporaId");
      recordRead.should.have.property("sourceFileName");
      recordRead.should.have.property("sourceFileSize");
      recordRead.should.have.property("createdAt");
      recordRead.should.have.property("trainedAt");

      // Created record should match with one being read
      recordWritten.corporaId.should.equal(recordRead.corporaId);
      recordWritten.createdAt.should.equal(recordRead.createdAt);
      recordRead.sourceFileName.should.equal(
        testCase.requestBody.source_file_name
      );
      recordRead.sourceFileSize.should.equal(
        testCase.requestBody.source_file_size
      );
    }
  });

  it("should update trained corpora info record and get the latest trained info", async () => {
    const { corporaInfo, fileName, fileSize } =
      await createCorporaInfoAndTasks();
    let res = await chai
      .request(RUUTER_URL)
      .post("/update_corpora_info")
      .send({ corpora_id: corporaInfo.corporaId });
    res.should.have.status(200);
    res.body.should.have.property("response");
    res.body.response.should.equal("success");

    res = await chai.request(RUUTER_URL).get("/trained_corpora_info");
    res.should.have.status(200);
    res.body.should.have.property("response");
    res.body.response.should.be.a("array").of.length(1);

    let recordRead = res.body.response.pop();
    recordRead.corporaId.should.equal(corporaInfo.corporaId);
    recordRead.createdAt.should.not.equal(corporaInfo.createdAt);
    expect(new Date(recordRead.createdAt) > new Date(corporaInfo.createdAt)).to
      .be.true;
    recordRead.sourceFileName.should.equal(fileName);
    recordRead.sourceFileSize.should.equal(fileSize);

    // Create a new corpora task record
    await createCorporaInfoAndTasks();

    // trained_corpora_info should return old corpora task record because new one is not trained yet.
    res = await chai.request(RUUTER_URL).get("/trained_corpora_info");
    res.should.have.status(200);
    res.body.should.have.property("response");
    res.body.response.should.be.a("array").of.length(1);

    recordRead = res.body.response.pop();
    recordRead.corporaId.should.equal(corporaInfo.corporaId);
    recordRead.createdAt.should.not.equal(corporaInfo.createdAt);
    expect(new Date(recordRead.createdAt) > new Date(corporaInfo.createdAt)).to
      .be.true;
    recordRead.sourceFileName.should.equal(fileName);
    recordRead.sourceFileSize.should.equal(fileSize);
  });

  it("should upload full corpus", async () => {
    const { tasksResponse, tasks } = await createCorporaInfoAndTasks();
    tasksResponse.should.have.status(200);
    tasksResponse.body.should.have.property("response");
    tasksResponse.body.response.should.be.a("array").of.length(tasks.length);
    for (let task of tasksResponse.body.response) {
      task.should.be.a("array").of.length(1);
      task[0].should.have.property("id");
    }
  });

  it("should read uploaded corpus with different pagination and sorting parameters", async () => {
    const { corporaInfo, tasksResponse, tasks } =
      await createCorporaInfoAndTasks();
    const savedTaskIds = tasksResponse.body.response.map((x) => x[0].id);
    let testCases = [
      {
        page_size: 2,
        where_condition: `corpora_id = '${corporaInfo.corporaId}'`,
        sort_condition: `Corpora_Tasks."id" ASC`,
      },
      {
        page_size: 2,
        where_condition: `corpora_id = '${corporaInfo.corporaId}'`,
        sort_condition: `Corpora_Tasks."id" DESC`,
      },
      {
        page_size: 3,
        where_condition: `corpora_id = '${corporaInfo.corporaId}'`,
        sort_condition: `Corpora_Tasks."id" DESC`,
      },
      {
        page_size: 30,
        where_condition: `corpora_id = '${corporaInfo.corporaId}'`,
        sort_condition: `Corpora_Tasks."id" DESC`,
      },
    ];
    for (let testCase of testCases) {
      let tasksResponse = [];
      for (let i = 1; i <= tasks.length / 2 + 1; i++) {
        res = await chai
          .request(RUUTER_URL)
          .get(`/tasks`)
          .query({ ...testCase, page: i });
        res.should.have.status(200);
        res.body.should.have.property("response");
        res.body.response.should.be
          .a("array")
          .of.length(
            tasks.length - tasksResponse.length > testCase.page_size
              ? testCase.page_size
              : tasks.length - tasksResponse.length
          );
        tasksResponse = tasksResponse.concat(res.body.response);
      }

      tasksResponse.should.be.a("array").of.length(tasks.length);
      for (let i = 0; i < tasksResponse.length; i++) {
        let task = tasksResponse[i];
        savedTaskIds.should.include(task.id);
        task.corporaId.should.equal(corporaInfo.corporaId);
        task.createdAt.should.equal(corporaInfo.createdAt);
        task.fullCount.should.equal(tasks.length);
        task.isPrivate.should.equal(true);
        task.rawText.should.equal(
          testCase.sort_condition === `Corpora_Tasks."id" ASC`
            ? tasks[i].raw_text
            : tasks.slice().reverse()[i].raw_text
        );
      }
    }
  });

  it("should read full uploaded corpus", async () => {
    const { corporaInfo, tasksResponse, tasks } =
      await createCorporaInfoAndTasks();
    const savedTaskIds = tasksResponse.body.response.map((x) => x[0].id);
    res = await chai.request(RESQL_URL).post(`/get_latest_corpora`);
    res.should.have.status(200);
    res.body.should.be.a("array").of.length(tasks.length);
    for (let i = 0; i < res.body.length; i++) {
      let task = res.body[i];
      savedTaskIds.should.include(task.id);
      task.corporaId.should.equal(corporaInfo.corporaId);
      task.createdAt.should.equal(corporaInfo.createdAt);
      task.fullCount.should.equal(tasks.length);
      task.isPrivate.should.equal(true);
      task.rawText.should.equal(tasks[i].raw_text);
    }
  });

  it("read a sentence", async () => {
    const { tasksResponse, corporaInfo, tasks } =
      await createCorporaInfoAndTasks();
    let query = {
      id: tasksResponse.body.response[0][0].id,
      project: corporaInfo.corporaId,
    };
    let res = await chai.request(RUUTER_URL).get(`/task`).query(query);
    res.should.have.status(200);
    res.body.should.have.property("response");
    const task = res.body.response;
    task.id.should.equal(tasksResponse.body.response[0][0].id);
    task.corporaId.should.equal(corporaInfo.corporaId);
    task.createdAt.should.equal(corporaInfo.createdAt);
    task.isPrivate.should.equal(tasks[0].is_private);
    task.rawText.should.equal(tasks[0].raw_text);
    expect(task.predictions === null).to.be.true;
  });

  it("annotate a sentence", async () => {
    const { tasksResponse, corporaInfo, tasks } =
      await createCorporaInfoAndTasks();
    let predictions = [
      JSON.stringify([
        {
          value: { start: 18, end: 23, text: "Urmas", labels: ["Nimi"] },
          id: "NqsFlYHoLX",
          from_name: "label",
          to_name: "text",
          type: "labels",
          origin: "manual",
        },
      ]),
      JSON.stringify([
        {
          value: { start: 20, end: 23, text: "Urmas", labels: ["Nimi"] },
          id: "NqsFlYHoLX",
          from_name: "label",
          to_name: "text",
          type: "labels",
          origin: "manual",
        },
      ]),
    ];
    for (let prediction of predictions) {
      let payload = {
        id: tasksResponse.body.response[0][0].id,
        sentences_annotations: prediction,
      };
      let res = await chai
        .request(RUUTER_URL)
        .post(`/annotate`)
        .query({ project: corporaInfo.corporaId })
        .send(payload);
      res.should.have.status(200);
      res.body.should.have.property("response");

      let query = {
        id: tasksResponse.body.response[0][0].id,
        project: corporaInfo.corporaId,
      };
      res = await chai.request(RUUTER_URL).get(`/task`).query(query);
      res.should.have.status(200);
      res.body.should.have.property("response");
      const task = res.body.response;
      task.id.should.equal(tasksResponse.body.response[0][0].id);
      task.corporaId.should.equal(corporaInfo.corporaId);
      task.createdAt.should.not.equal(corporaInfo.createdAt);
      expect(new Date(task.createdAt) > new Date(corporaInfo.createdAt)).to.be
        .true;
      task.isPrivate.should.equal(tasks[0].is_private);
      task.rawText.should.equal(tasks[0].raw_text);
      task.predictions.should.equal(prediction);
    }
  });

  it("should create and read entity records", async () => {
    //Fresh DB State should have no data.
    let res = await chai.request(RUUTER_URL).get("/entity");
    res.should.have.status(200);
    res.body.should.have.property("response");
    res.body.response.should.be.a("array").of.length(0);

    let testCases = [
      {
        requestBody: {
          name: "Name",
          description: "Name",
        },
      },
      {
        requestBody: {
          name: "Place",
          description: "Place",
        },
      },
    ];
    let latestResponse = [];
    for (let i = 0; i < testCases.length; i++) {
      const testCase = testCases[i];
      res = await chai
        .request(RUUTER_URL)
        .post("/entity")
        .send(testCase.requestBody);
      res.should.have.status(200);
      res.body.should.have.property("response");
      res.body.response.should.equal("success");

      res = await chai.request(RUUTER_URL).get("/entity");
      res.should.have.status(200);
      res.body.should.have.property("response");
      res.body.response.should.be.a("array").of.length(i + 1);
      latestResponse = [...res.body.response];
      const recordRead = res.body.response.pop();
      recordRead.should.have.property("name");
      recordRead.should.have.property("description");

      recordRead.name.should.equal(testCase.requestBody.name);
      recordRead.description.should.equal(testCase.requestBody.description);
    }
    latestResponse.should.be.a("array").of.length(testCases.length);
  });

  it("should create, read and delete regex records", async () => {
    //Fresh DB State should have no data.
    let res = await chai.request(RUUTER_URL).get("/regex");
    res.should.have.status(200);
    res.body.should.have.property("response");
    res.body.response.should.be.a("array").of.length(0);

    let testCases = [
      {
        requestBody: {
          entity: "color",
          regex: "colou?r",
        },
      },
      {
        requestBody: {
          entity: "gray",
          regex: "gr[ae]y",
        },
      },
    ];
    let latestResponse = [];
    for (let i = 0; i < testCases.length; i++) {
      const testCase = testCases[i];
      res = await chai
        .request(RUUTER_URL)
        .post("/regex")
        .send(testCase.requestBody);
      res.should.have.status(200);
      res.body.should.have.property("response");
      res.body.response.should.be.a("array").of.length(1);
      const id = res.body.response[0].id;
      res = await chai.request(RUUTER_URL).get("/regex");
      res.should.have.status(200);
      res.body.should.have.property("response");
      res.body.response.should.be.a("array").of.length(i + 1);
      latestResponse = [...res.body.response];
      const recordRead = res.body.response.pop();
      recordRead.should.have.property("id");
      recordRead.should.have.property("entity");
      recordRead.should.have.property("regex");

      recordRead.id.should.equal(id);
      recordRead.entity.should.equal(testCase.requestBody.entity);
      recordRead.regex.should.equal(testCase.requestBody.regex);
    }
    latestResponse.should.be.a("array").of.length(testCases.length);
    for (let i = 0; i < latestResponse.length; i++) {
      const testCase = latestResponse[i];
      let res = await chai
        .request(RUUTER_URL)
        .get(`/delete_regex`)
        .query({ id: testCase.id });
      res.should.have.status(200);
      res.body.should.have.property("response");
      res.body.response.should.equal("success");
      res = await chai.request(RUUTER_URL).get("/regex");
      res.body.response.should.be
        .a("array")
        .of.length(latestResponse.length - (i + 1));
      expect(res.body.response.find((x) => x.id === testCase.id)).to.be
        .undefined;
    }
  });
});

async function createCorporaInfoAndTasks() {
  const fileName = "korpus_test.txt";
  const fileSize = `${fs.statSync(fileName).size}`;
  const corporaInfo = (
    await chai.request(RUUTER_URL).post("/corpora_info").send({
      source_file_name: fileName,
      source_file_size: fileSize,
    })
  ).body.response.pop();
  const tasks = fs
    .readFileSync(fileName)
    .toString()
    .split("\n")
    .map((sentence) => ({
      raw_text: sentence,
      corpora_id: corporaInfo.corporaId,
      is_private: true,
      created_at: corporaInfo.createdAt,
    }));
  let tasksResponse = await chai.request(RUUTER_URL).post("/corpora").send({
    tasks,
  });
  return { fileName, fileSize, corporaInfo, tasks, tasksResponse };
}
