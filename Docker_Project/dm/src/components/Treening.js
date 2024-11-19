import styled from "styled-components";
import {
  Button,
  Input,
  Select,
  Modal,
  notification,
  Table,
  Tag,
  Upload,
  Progress,
} from "antd";
import { Link } from "react-router-dom";
import { useState, useEffect, useRef } from "react";
import GithubSection from "./GithubSection";
import UploadIcon from "../assets/upload.svg";
import DropdownIcon from "../assets/dropdown.svg";
import CheckIcon from "../assets/Check.svg";
import AddIcon from "../assets/Add.svg";
import CloseIcon from "../assets/close.svg";
import CloseRedIcon from "../assets/close_red.svg";
import CopyIcon from "../assets/Copy.svg";
import LoopIcon from "../assets/Loop.svg";
import {
  uploadCorpus,
  fetchPreLabellingStatus,
  startTraining,
  fetchTrainingStatus,
  annotateCorpora,
  listRegex,
  deleteRegex,
  deleteCorporaInfo,
  createRegex,
  getEntities,
  createEntity,
  getCorporaInfo,
  addCorporaInfo,
  getTrainedCorporaInfo,
} from "../RestService";
import { useTranslation } from "react-i18next";

const LABEL_STUDIO_URL = process.env.REACT_APP_LABEL_STUDIO_URL;
const getFormattedDate = (d) =>
  `${d.getDate().toString().padStart(2, "0")}.${d
    .getMonth()
    .toString()
    .padStart(2, "0")}.${d.getFullYear().toString().padStart(2, "0")} ${d
    .getHours()
    .toString()
    .padStart(2, "0")}:${d.getMinutes().toString().padStart(2, "0")}:${d
    .getSeconds()
    .toString()
    .padStart(2, "0")}`;

const { TextArea } = Input;

const UploadSection = styled.div`
  padding: 48px 149px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  @media (max-width: 746px) {
    padding: 24px 16px;
  }
`;

const RegexSection = styled.div`
  padding: 48px 149px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  background: #f2f2fe;
  @media (max-width: 746px) {
    padding: 24px 16px;
  }
`;

const Title = styled.div`
  font-size: 48px;
  font-weight: 300;
  color: #808284;
  font-family: Aino-Headline;
  @media (max-width: 680px) {
    font-style: normal;
    font-weight: 400;
    font-size: 32px;
    line-height: 120%;
  }
`;

const UploadContainer = styled.div`
  font-size: 50px;
  font-weight: 300;
  color: #808284;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: #F2F2FE;
  border: 1px dashed #CFD1D2;
  border-radius: 10px;
  max-width: 555px;
  width: 100%;
  // margin: 48px 0px;
  margin-top: 48px;
  padding 56px;
  @media (max-width: 746px) {
    max-width: unset;
    margin-top: 16px;
    width: 100%;
  }
`;

const UploadingETAContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 56px;
  background: rgba(242, 242, 254, 0.5);
  border-radius: 10px;
  box-sizing: border-box;
  // margin: 48px 0px;
  margin-top: 48px;
  width: 555px;
`;

const UploadHeading = styled.div`
  font-style: normal;
  font-weight: 700;
  font-size: 16px;
  line-height: 24px;
  color: #323334;
  margin-top: 24px;
`;

const UploadDescription = styled.div`
  font-style: normal;
  font-weight: 400;
  font-size: 14px;
  line-height: 20px;
  color: #575a5d;
  margin-top: 8px;
  margin-bottom: 24px;
`;

const ThemeButtonContainer = styled.div`
  display: flex;
  align-items: center;
  margin-top: 24px;
  flex-wrap: wrap;
  gap: 16px;
  @media (max-width: 746px) {
    margin-top: 16px !important;
  }
`;

const ThemeButton = styled(Button)`
  border-radius: 100px !important;
  background-color: ${(props) =>
    props.disabled ? "#575A5D" : "#0000F0"} !important;
  color: white !important;
  //  margin-right: 16px;
  border: ${(props) =>
    props.disabled ? "2px solid #575A5D" : "2px solid #0000e7"} !important;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  line-height: 16px;
  font-weight: 700;
  height: 40px;
  padding: 12px 18px;
  &:hover {
    filter: brightness(200%) !important;
  }
`;

const ThemeButton2 = styled(Button)`
  border-radius: 100px !important;
  background-color: transparent !important;
  color: ${(props) => (props.disabled ? "#575A5D" : "#003CFF")} !important;
  border: ${(props) =>
    props.disabled ? "2px solid #CFD1D2" : "2px solid #003CFF"} !important;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  line-height: 16px;
  font-weight: 700;
  height: 40px;
  padding: 12px 18px;
  &:hover {
    filter: brightness(200%) !important;
  }
`;

const ThemeButton3 = styled(Button)`
  padding: 8px 16px;
  background: #df4300 !important;
  border-radius: 100px !important;
  font-style: normal;
  font-weight: 700;
  font-size: 12px;
  line-height: 16px;
  letter-spacing: 0.5px;
  color: #ffffff !important;
  border: 2px solid #df4300 !important;
  margin-right: 13px;
  display: flex;
  align-items: center;
  &:hover {
    filter: brightness(120%) !important;
  }
`;

const ThemeButton4 = styled(Button)`
  padding: 8px 16px;
  background: transparent !important;
  border-radius: 100px !important;
  font-style: normal;
  font-weight: 700;
  font-size: 12px;
  line-height: 16px;
  letter-spacing: 0.5px;
  color: #003cff !important;
  border: 2px solid #003cff !important;
  display: flex;
  align-items: center;
  &:hover {
    filter: brightness(200%) !important;
  }
`;

const AddEntityInput = styled(Input)`
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 12px 16px;
  height: 48px;
  background: #ffffff;
  border: 1px solid #cfd1d2;
  border-radius: 4px;
  ::placeholder {
    font-style: normal;
    font-weight: 400;
    font-size: 16px;
    line-height: 24px;
    color: #575a5d;
  }
  font-style: normal;
  font-weight: 400;
  font-size: 16px;
  line-height: 24px;
  color: #000000;
`;

const RegexTextArea = styled(TextArea)`
  height: 235px;
  max-height: 235px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 16px;
  background: #ffffff;
  border: 1px solid #cfd1d2;
  border-radius: 4px;
  ::placeholder {
    font-style: normal;
    font-weight: 400;
    font-size: 16px;
    line-height: 24px;
    color: #575a5d;
  }
  font-style: normal;
  font-weight: 400;
  font-size: 16px;
  line-height: 24px;
  color: #000000;
`;

const RegexAreaContainer = styled.div`
  display: flex;
  width: 100%;
  gap: 32px;
  flex-wrap: wrap;
  margin-top: 24px;
  @media (max-width: 985px) {
    gap: 48px;
  }
`;

const TextAreaGap = styled.div`
  width: 32px;
  display: flex;
`;

const EntitySection = styled.div`
  // width: calc(50% - 16px);
  // width: 100%;
  flex: 1;
  min-width: 328px;
  display: flex;
  flex-direction: column;
  @media (max-width: 329px) {
    min-width: unset;
  }
`;

const RegexAreaSection = styled.div`
  display: flex;
  flex-direction: column;
  // width: calc(50% - 16px);
  // width: 100%;
  flex: 1;
  min-width: 328px;
  @media (max-width: 329px) {
    min-width: unset;
  }
`;

const RegexNotationText = styled.div`
  margin-top: 8px;
  font-style: normal;
  font-weight: 400;
  font-size: 14px;
  line-height: 20px;
  color: #575a5d;
`;

const InputHeading = styled.div`
  // flex: 1;
  text-align: left;
  font-style: normal;
  font-weight: 700;
  font-size: 14px;
  line-height: 20px;
  color: #323334;
  margin-bottom: 8px;
`;

const SelectEntity = styled(Select)`
  width: 100%;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  border-radius: 4px;
  height: 48px !important;
  .ant-select-selection-item {
    align-self: center;
    font-style: normal;
    font-weight: 400;
    font-size: 16px;
    line-height: 24px;
  }
  .ant-select-selector {
    border: 1px solid #cfd1d2 !important;
    border-radius: 4px !important;
    height: 48px !important;
    padding: 0 16px !important;
    box-shadow: none !important;
  }
  .ant-select-selection-placeholder {
    font-style: normal;
    font-weight: 400;
    font-size: 16px;
    line-height: 24px;
    display: flex;
    align-items: center;
    color: #575a5d;
  }
  .ant-select-arrow {
    right: 16px !important;
  }
`;

const RegexTable = styled(Table)`
  th {
    font-weight: bold !important;
    font-size: 14px !important;
    font-style: normal !important;
    font-weight: 700 !important;
    font-size: 12px !important;
    line-height: 16px !important;
    letter-spacing: 0.5px !important;
    color: #0000f0 !important;
  }
  tbody {
    tr {
      @media (max-width: 900px) {
        display: flex;
        flex-direction: column;
        border-bottom: 1px solid #f0f1f2;
        padding: 24px 0px;
      }
      td {
        padding: 10px 16px;
        @media (max-width: 900px) {
          border-bottom: none;
        }
      }
    }
  }
  .ant-table-body {
    max-height: calc(100vh - 250px) !important;
  }
  .ant-table-row {
    height: 56px !important;
  }
  col: {
    display: none !important;
  }
  @media (max-width: 900px) {
    th {
      display: none !important;
    }
    .ant-table-measure-row {
      display: none !important;
    }
    .ant-table-row {
      height: 100% !important;
    }
  }
`;

const ColumnMuster = styled.div`
  font-style: normal;
  font-weight: 400;
  font-size: 14px;
  line-height: 16px;
  color: #323334;
`;

const ColumnNimetus = styled.div`
  font-style: normal;
  font-weight: 400;
  font-size: 14px;
  line-height: 20px;
  color: #323334;
`;

const ConfirmDeleteRegexContainer = styled.div`
  display: flex;
  position: relative;
  right: 74px;
  @media (max-width: 900px) {
    position: absolute;
    right: 16px;
  }
`;

const RegexModalActions = styled.div`
  display: flex;
  @media (max-width: 900px) {
    justify-content: space-between;
  }
`;

const RegexModalAction = styled.div`
  font-style: normal;
  font-weight: 400;
  font-size: 16px;
  line-height: 24px;
  letter-spacing: 0.5px;
  color: #df4300;
  cursor: pointer;
  display: flex;
  align-items: center;
  margin: 0 16px;
  @media (max-width: 900px) {
    margin: 0;
  }
  &:hover {
    filter: brightness(120%) !important;
  }
`;

const UploadAttachmentInfo = styled.div`
  width: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 16px;
  background: #ffffff;
  border-radius: 6px;
  margin-top: 27px;
`;

const UploadAttachmentInfoColumns = styled.div`
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const UploadText = styled.div`
  font-style: normal;
  font-weight: 400;
  font-size: 14px;
  line-height: 20px;
  color: #000000;
`;

const FileStatus = styled.div`
  font-style: normal;
  font-weight: 400;
  font-size: 14px;
  line-height: 20px;
  color: #067f3e;
`;

const Description = styled.div`
  font-style: normal;
  font-weight: 400;
  font-size: 18px;
  line-height: 28px;
  color: #323334;
  margin-top: 16px;
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
`;

const BrandLink = styled(Link)`
  color: #0000f0 !important;
  text-decoration: underline !important;
`;

const FileTag = styled(Tag)`
  padding: 4px 8px 2px;
  background: #f0f1f2;
  border-radius: 4px;
  font-style: normal;
  font-weight: 400;
  font-size: 18px;
  line-height: 28px;
  text-decoration-line: underline;
  color: #0000f0;
  margin: 0 4px;
`;

const ETA = styled.div`
  padding: 4px 10px;
  background: #ffffff;
  border-radius: 100px;
  font-style: normal;
  font-weight: 700;
  font-size: 12px;
  line-height: 16px;
  display: flex;
  align-items: center;
  text-align: center;
  color: #0000f0;
  margin-top: 3px;
  margin-bottom: 24px;
`;

const TrainingStatus = styled.div`
  padding: 4px 8px;
  background: #f9e7f2;
  border-radius: 100px;
  font-style: normal;
  font-weight: 400;
  font-size: 14px;
  line-height: 20px;
  color: #df4300;
  margin-bottom: 4px;
`;

const DeleteCorporaButton = styled.img`
  margin-right: 4px;
  transform: rotate(270deg);
  ${(props) => props.disabled ? "" : "cursor: pointer;"} 
  ${(props) => props.disabled ? "opacity: 0.5;" : ""}
`

function Treening() {
  const [entityModalOpened, setEntityModalOpened] = useState(false);
  const [entityText, setEntityText] = useState("");
  const [entityDescription, setEntityDescription] = useState("");
  const [uploadingState, setUploadingState] = useState(1);
  const [regexModalOpened, setRegexModalOpened] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [file, setFile] = useState(null);
  const [createRegexText, setCreateRegexText] = useState("");
  const [selectedEntity, setSelectedEntity] = useState(null);
  const [entities, setEntities] = useState([]);
  const [tableData, setTableData] = useState([]);
  const [corporaInfo, setCorporaInfo] = useState(null);
  const [trainedCorporaInfo, setTrainedCorporaInfo] = useState(null);
  const { t } = useTranslation("common");

  const annotateCorporaAndPollStatus = async () => {
    let response = await annotateCorpora();
    notification.info({
      description: "Prelabelling started. Please wait...",
      placement: "bottomLeft",
      icon: <div />,
      closeIcon: <div />,
    });
    let timer = setInterval(() => {
      fetchPreLabellingStatus(response.task_id).then((status) => {
        if (status.task_status === "SUCCESS") {
          clearInterval(timer);
          notification.info({
            description: "Prelabelling successfully completed!",
            placement: "bottomLeft",
            icon: <div />,
            closeIcon: <div />,
          });
          setTimeout(
            () => window.open(LABEL_STUDIO_URL, "_blank").focus(),
            1000
          );
        }
      });
    }, 5000);
  };

  const deleteRegexRecord = async (record) => {
    let response = await deleteRegex(record.id);
    if (response === "success") {
      notification.info({
        description: t("trainingPage.regexRemovedText"),
        placement: "bottomLeft",
        icon: <div />,
        closeIcon: <div />,
      });
      let tempData = JSON.parse(JSON.stringify(tableDataRef.current));
      tempData = tempData.filter((regexRecord) => regexRecord.id !== record.id);
      setTableData(tempData);
      tableDataRef.current = tempData;
    }
  };

  const deleteCorpora = async () => {
    if (!corporaInfo) return;
    if (corporaInfo.countt === 1) return;
    let response = await deleteCorporaInfo(corporaInfo?.corporaId);
    if (response === "success") {
      notification.info({
        description: t("trainingPage.deleteTrainingFile"),
        placement: "bottomLeft",
        icon: <div />,
        closeIcon: <div />,
      });
      getCorporaInfo().then((res) => {
        if (res.length === 0) return;
        else if (!res[0].trainedAt) setUploadingState(3);
        setCorporaInfo(res[0]);
      });
      setUploadingState(1);
    }
  };

  const createEntityRecord = async () => {
    const response = await createEntity(entityText, entityDescription);
    if (response === "success") {
      setEntities([
        ...JSON.parse(JSON.stringify(entities)),
        {
          name: entityText,
          description: entityDescription,
        },
      ]);
    }
  };

  const createRegexRecord = async () => {
    let response = await createRegex(createRegexText, selectedEntity);
    if (response?.[0]?.id) {
      let tempData = JSON.parse(JSON.stringify(tableDataRef.current));
      tempData.push({
        id: response[0].id,
        muster: createRegexText,
        nimetus: selectedEntity,
        confirmingDelete: false,
      });
      setTableData(tempData);
      tableDataRef.current = tempData;
      setCreateRegexText("");
      notification.info({
        description: t("trainingPage.regexSavedText"),
        placement: "bottomLeft",
        icon: <div />,
        closeIcon: <div />,
      });
    }
  };

  useEffect(() => {
    if (uploadingState === 4) {
      let timer = setInterval(() => {
        fetchTrainingStatus().then((status) => {
          if (["Failed", "Done", "Standby"].includes(status?.status)) {
            setUploadingState(1);
            getTrainedCorporaInfo().then((res) =>
              setTrainedCorporaInfo(res[0])
            );
            clearInterval(timer);
          }
        });
      }, 10000);
    }
  }, [uploadingState]);

  useEffect(() => {
    fetchTrainingStatus().then((status) => {
      // if (!["Failed", "Done", "Standby"].includes(status?.status)) {
      //   setUploadingState(4);
      // }
    });
    listRegex().then((regexes) => {
      tableDataRef.current = regexes.map((regexRecord) => ({
        id: regexRecord.id,
        muster: regexRecord.regex,
        nimetus: regexRecord.entity,
        confirmingDelete: false,
      }));
      setTableData(tableDataRef.current);
    });
    getEntities().then(setEntities);
    getCorporaInfo().then((res) => {
      setCorporaInfo(res[0]);
      if (res.length === 0) return;
      else if (!res[0].trainedAt) setUploadingState(3);
    });
    getTrainedCorporaInfo().then((res) => setTrainedCorporaInfo(res[0]));
  }, []);

  const tableDataRef = useRef(tableData);

  const [columns, setColumns] = useState([
    {
      dataIndex: "muster",
      key: "muster",
      title: t("trainingPage.regexTableColumn"),
      width: 331,
      render(text, record, index) {
        return {
          children: (
            <ColumnMuster
              style={{ opacity: record.confirmingDelete ? 0.2 : 1 }}
            >
              {text}
            </ColumnMuster>
          ),
        };
      },
    },
    {
      render(text, record, index) {
        return {
          children: (
            <ColumnNimetus
              style={{ opacity: record.confirmingDelete ? 0.2 : 1 }}
            >
              {text}
            </ColumnNimetus>
          ),
        };
      },
      title: () => (
        <div style={{ marginLeft: 20 }}>
          {t("trainingPage.regexEntityColumn")}
        </div>
      ),
      width: 202,
      dataIndex: "nimetus",
      key: "nimetus",
      defaultSortOrder: "descend",
      sorter: (a, b) => a.nimetus.localeCompare(b.nimetus),
    },
    {
      render(text, record, index) {
        return {
          children: (
            <RegexModalActions>
              <RegexModalAction
                style={{
                  color: "#0000F0",
                  opacity: record.confirmingDelete ? 0.2 : 1,
                }}
                onClick={() => {
                  navigator.clipboard.writeText(record.muster);
                  notification.info({
                    description: t("trainingPage.regexCopiedText"),
                    placement: "bottomLeft",
                    icon: <div />,
                    closeIcon: <div />,
                  });
                }}
              >
                <img src={CopyIcon} style={{ marginRight: 8 }} />
                {t("trainingPage.copyText")}
              </RegexModalAction>
              <div style={{ marginLeft: 8 }} />
              {record.confirmingDelete ? (
                <ConfirmDeleteRegexContainer>
                  <ThemeButton3
                    onClick={() => {
                      let tempData = JSON.parse(
                        JSON.stringify(tableDataRef.current)
                      );
                      tempData.find(
                        (x) => x.id === record.id
                      ).confirmingDelete = false;
                      setTableData(tempData);
                      tableDataRef.current = tempData;
                      deleteRegexRecord(record);
                    }}
                  >
                    {t("trainingPage.confirm")}
                  </ThemeButton3>
                  <ThemeButton4
                    onClick={() => {
                      let tempData = JSON.parse(
                        JSON.stringify(tableDataRef.current)
                      );
                      tempData.find(
                        (x) => x.id === record.id
                      ).confirmingDelete = false;
                      setTableData(tempData);
                      tableDataRef.current = tempData;
                    }}
                  >
                    {t("trainingPage.cancel")}
                  </ThemeButton4>
                </ConfirmDeleteRegexContainer>
              ) : (
                <RegexModalAction
                  onClick={() => {
                    let tempData = JSON.parse(
                      JSON.stringify(tableDataRef.current)
                    );
                    for (let i = 0; i < tempData.length; i++) {
                      tempData[i].confirmingDelete = false;
                    }
                    tempData.find(
                      (x) => x.id === record.id
                    ).confirmingDelete = true;
                    setTableData(tempData);
                    tableDataRef.current = tempData;
                  }}
                >
                  <img src={CloseRedIcon} style={{ marginRight: 8 }} />
                  {t("trainingPage.remove")}
                </RegexModalAction>
              )}
            </RegexModalActions>
          ),
        };
      },
    },
  ]);

  const handleUpload = async (file) => {
    const reader = new FileReader();

    reader.onload = async (e) => {
      try {
        setUploadingState(2);
        let corpus = e.target.result.split("\n").filter((x) => x !== "");
        let totalChunks = corpus.length / 100;
        let currentChunk = 0;
        setUploadProgress(0);
        const corpusInfo = (await addCorporaInfo(file.name, file.size))?.[0];
        setCorporaInfo({
          ...corpusInfo,
          sourceFileName: file.name,
          sourceFileSize: file.size,
          created_at: corpusInfo.createdAt,
          countt: (corporaInfo?.countt || 0) + 1,
        });
        for (let i = 0; i < corpus.length; i += 100) {
          let chunk = corpus.slice(i, i + 100);
          chunk = {
            tasks: chunk.map((sentence) => ({
              raw_text: sentence,
              corpora_id: corpusInfo.corporaId,
              is_private: true,
              created_at: corpusInfo.createdAt,
            })),
          };
          if (chunk.tasks.length) await uploadCorpus(chunk);
          currentChunk++;
          setUploadProgress(Math.round((currentChunk / totalChunks) * 100));
        }
        setUploadProgress(100);
        setUploadingState(3);
      } catch (err) {
        console.log(err);
      }
    };
    reader.readAsText(file);
    setFile(file);
    return false;
  };

  return (
    <>
      <Modal
        maskStyle={{ background: "rgba(0, 0, 135, 0.75)" }}
        closeIcon={<img src={CloseIcon} />}
        width={520}
        close
        onCancel={() => {
          setEntityModalOpened(false);
          setEntityText("");
          setEntityDescription("");
        }}
        title={t("trainingPage.addEntityModalTitle")}
        open={entityModalOpened}
        footer={
          <ThemeButton
            disabled={!(entityText && entityDescription)}
            onClick={() => {
              createEntityRecord();
              setEntityModalOpened(false);
              setEntityText("");
              setEntityDescription("");
            }}
          >
            {t("trainingPage.saveButton")}
          </ThemeButton>
        }
      >
        <InputHeading>{t("trainingPage.entityName")}</InputHeading>
        <AddEntityInput
          value={entityText}
          onChange={(ev) => setEntityText(ev.target.value)}
          placeholder={t("trainingPage.enterInputPlaceholder")}
        />
        <InputHeading style={{ marginTop: 12 }}>
          {t("trainingPage.entityDescription")}
        </InputHeading>
        <RegexTextArea
          value={entityDescription}
          onChange={(ev) => setEntityDescription(ev.target.value)}
          placeholder={t("trainingPage.enterInputPlaceholder")}
        />
      </Modal>

      <Modal
        maskStyle={{ background: "rgba(0, 0, 135, 0.75)" }}
        closeIcon={<img src={CloseIcon} />}
        width={866}
        close
        onCancel={() => setRegexModalOpened(false)}
        title={t("trainingPage.regexModalTitle")}
        open={regexModalOpened}
        footer={
          <ThemeButton onClick={() => setRegexModalOpened(false)}>
            {t("trainingPage.regexModalClose")}
          </ThemeButton>
        }
      >
        <RegexTable
          id="regexTable"
          scroll={{
            y: 300,
          }}
          pagination={false}
          dataSource={tableData}
          columns={columns}
        />
      </Modal>
      <GithubSection />
      <UploadSection>
        <Title>{t("trainingPage.title")}</Title>
        <Description>
          {trainedCorporaInfo?.trainedAt ? (
            <>
              Mudel failinimega
              <FileTag>{trainedCorporaInfo?.sourceFileName}</FileTag>
              on treenitud{" "}
              {trainedCorporaInfo?.trainedAt &&
                getFormattedDate(new Date(trainedCorporaInfo.trainedAt))}
            </>
          ) : (
            t("trainingPage.usePublicModel")
          )}
        </Description>
        {uploadingState === 4 ? (
          <UploadingETAContainer>
            <img src={LoopIcon} />
            <UploadHeading>
              {t("trainingPage.trainingInProgress")}
            </UploadHeading>
            <UploadDescription>
              private-corpus-2022-11-03-11-11-11.ext
            </UploadDescription>
            <ETA>
              {t("trainingPage.ETA")}: 15 {t("trainingPage.seconds")}
            </ETA>
            <TrainingStatus>{t("trainingPage.trainingStatus")}</TrainingStatus>
          </UploadingETAContainer>
        ) : (
          <UploadContainer>
            <img src={UploadIcon} />
            <UploadHeading>{t("trainingPage.uploadTitle")}</UploadHeading>
            <UploadDescription>
              {t("trainingPage.uploadDescription")}
            </UploadDescription>
            {uploadingState === 2 && (
              <Progress strokeColor="#0000F0" percent={uploadProgress} />
            )}
            {uploadingState < 4 ? (
              <Upload showUploadList={false} beforeUpload={handleUpload}>
                <ThemeButton disabled={uploadingState === 2}>
                  {t(
                    uploadingState < 3
                      ? "trainingPage.uploadButton"
                      : "trainingPage.uploadAgainButton"
                  )}
                </ThemeButton>{" "}
              </Upload>
            ) : (
              <div />
            )}
            {uploadingState === 3 && (
              <UploadAttachmentInfo>
                <UploadAttachmentInfoColumns>
                  <div>
                    <UploadText>{corporaInfo?.sourceFileName}</UploadText>
                    <FileStatus>
                      {t("trainingPage.uploadSuccessButton")}
                    </FileStatus>
                  </div>
                  <UploadText>
                    {Math.round((corporaInfo?.sourceFileSize / 1000000) * 100) /
                      100}{" "}
                    {t("trainingPage.mb")}
                  </UploadText>
                  <DeleteCorporaButton
                    title={t("trainingPage.deleteCorporaButtonTitle")}
                    onClick={deleteCorpora}
                    src={CloseIcon}
                    disabled={corporaInfo.countt === 1}
                  />
                </UploadAttachmentInfoColumns>
              </UploadAttachmentInfo>
            )}
          </UploadContainer>
        )}

        {(uploadingState === 3 || uploadingState === 4) && (
          <ThemeButtonContainer style={{ marginTop: 48 }}>
            <ThemeButton
              onClick={() => {
                startTraining();
                setUploadingState(4);
              }}
              disabled={uploadingState === 4}
            >
              {t("trainingPage.trainingButton")}
            </ThemeButton>
            <UploadText style={{ marginRight: 16 }}>
              {t("trainingPage.or")}
            </UploadText>
            <ThemeButton2
              onClick={annotateCorporaAndPollStatus}
              disabled={uploadingState === 4}
              style={{ marginRight: 16 }}
            >
              {t("trainingPage.preAnnotateButton")}
            </ThemeButton2>
            <ThemeButton2
              onClick={() => window.open(LABEL_STUDIO_URL, "_blank").focus()}
              disabled={uploadingState === 4}
            >
              {t("trainingPage.openLabellingPage")}
            </ThemeButton2>
          </ThemeButtonContainer>
        )}
      </UploadSection>
      <RegexSection>
        <Title>{t("trainingPage.regexSectionTitle")}</Title>
        <Description style={{ display: "block" }}>
          {t("trainingPage.regexSectionDescription")}{" "}
          <BrandLink
            to="https://github.com/buerokratt/Data-Anonymizer/blob/main/GUIDE.md"
            target="_blank"
            rel="noopener noreferrer"
          >
            {t("trainingPage.regexSectionDescriptionLink")}
          </BrandLink>
        </Description>

        <RegexAreaContainer>
          <RegexAreaSection>
            <InputHeading>{t("trainingPage.regexInputLabel")}</InputHeading>
            <RegexTextArea
              value={createRegexText}
              onChange={(ev) => setCreateRegexText(ev.target.value)}
              rows={10}
            />
            <RegexNotationText>
              {t("trainingPage.regexNotation")}
            </RegexNotationText>
            <ThemeButtonContainer>
              <ThemeButton
                disabled={!createRegexText || !selectedEntity}
                onClick={createRegexRecord}
              >
                {t("trainingPage.saveRegexButton")}
              </ThemeButton>
            </ThemeButtonContainer>
          </RegexAreaSection>
          {/* <TextAreaGap /> */}
          <EntitySection>
            <InputHeading>
              {t("trainingPage.entitySelectionLabel")}
            </InputHeading>
            <SelectEntity
              menuItemSelectedIcon={<img src={CheckIcon} />}
              suffixIcon={<img src={DropdownIcon} />}
              value={selectedEntity}
              onChange={setSelectedEntity}
              placeholder={t("trainingPage.selectEntityPlaceholder")}
            >
              {entities.map((entity) => (
                <Select.Option value={entity.name} />
              ))}
            </SelectEntity>
            <ThemeButtonContainer>
              <ThemeButton onClick={() => setEntityModalOpened(true)}>
                <img style={{ marginRight: 8 }} src={AddIcon} />
                {t("trainingPage.createEntityButton")}
              </ThemeButton>
              <ThemeButton2 onClick={() => setRegexModalOpened(true)}>
                {t("trainingPage.openRegexModal")}
              </ThemeButton2>
            </ThemeButtonContainer>
          </EntitySection>
        </RegexAreaContainer>
      </RegexSection>
    </>
  );
}

export default Treening;
