import styled from "styled-components";
import { Input, Button, Card, notification, Modal, Table, Tag } from "antd";
import { useState, useEffect } from "react";
import KeywordTag from "./KeywordTag";
import GithubSection from "./GithubSection";
import CloseIcon from "../assets/close.svg";
import RightIcon from "../assets/Right_Icon.svg";
import { pseudonymiseText, getEntities } from "../RestService";

function pickTextColorBasedOnBgColorAdvanced(bgColor, lightColor, darkColor) {
  var color = bgColor.charAt(0) === "#" ? bgColor.substring(1, 7) : bgColor;
  var r = parseInt(color.substring(0, 2), 16); // hexToR
  var g = parseInt(color.substring(2, 4), 16); // hexToG
  var b = parseInt(color.substring(4, 6), 16); // hexToB
  var uicolors = [r / 255, g / 255, b / 255];
  var c = uicolors.map((col) => {
    if (col <= 0.03928) {
      return col / 12.92;
    }
    return Math.pow((col + 0.055) / 1.055, 2.4);
  });
  var L = 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
  return L > 0.179 ? darkColor : lightColor;
}

const { TextArea } = Input;

const entityColors = [
  "#6DC0F7",
  "#C8C8C8",
  "#F1A17A",
  "#0000E6",
  "#5CB8AB",
  "#CE4F23",
  "#58C1DC",
];

const tagColors = [
  "#A0E432",
  "#4AC3FC",
  "#29BBAB",
  "#DF9BFF",
  "#FF9C72",
  "#FCFF62",
];

const Container = styled.div`
  background: #f2f2fd;
  padding: 48px 150px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  @media (max-width: 680px) {
    padding: 24px 16px;
  }
`;

const Title = styled.div`
  font-size: 48px;
  line-height: 56px;
  font-style: normal;
  font-weight: 400;
  font-family: Aino-Headline;
  margin-bottom: 16px;
  @media (max-width: 680px) {
    font-style: normal;
    font-weight: 400;
    font-size: 32px;
    line-height: 120%;
  }
`;

const AnonymizerTextContainer = styled.div`
  display: flex;
  width: 100%;
  flex-wrap: wrap;
  // gap: 32px;
  margin-top: 48px;
  @media (max-width: 987px) {
    margin-top: 16px;
  }
`;

const AnonymizerTextHeadingContainer = styled.div`
  display: flex;
  width: 100%;
  margin-top: 48px;
`;

const AnonymizerTextArea = styled(TextArea)`
  // flex: 1;
  height: 235px;
  max-height: 235px;
  // min-width: 328px;
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

const ThemeButton = styled(Button)`
  border-radius: 100px !important;
  background-color: ${(props) =>
    props.disabled ? "#575A5D" : "#0000F0"} !important;
  color: white !important;
  margin-right: 16px;
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

const AnonymizerTextCardContainer = styled.div`
  flex: 1;
  // min-width: 328px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
`;

const AnonymizerTextCard = styled(Card)`
  // flex: 1;
  // min-width: 328px;
  cursor: text;
  overflow: scroll;
  flex-direction: row;
  text-align: left;
  padding: 10px;
  border: 1px solid #d9d9d9;
  .ant-card-body {
    flex-wrap: wrap;
    overflow: scroll;
    padding: 0px;
    display: flex;
  }
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 16px;
  height: 238px;
  border: 1px solid #cfd1d2;
  border-radius: 4px;
  font-style: normal;
  font-weight: 400;
  font-size: 16px;
  line-height: 24px;
  color: #000000;
`;

const AnonymizerTextCount = styled.div`
  text-align: right;
  margin-top: 8px;
  font-style: normal;
  font-weight: 400;
  font-size: 14px;
  line-height: 20px;
  color: #575a5d;
`;

const AnonymizerTextAreaGap = styled.div`
  width: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 238px;
  margin-top: 27px;
  @media (max-width: 987px) {
    width: 100%;
    height: unset;
    margin: 24px 0px;
    transform: rotate(90deg);
  }
`;

const InputHeading = styled.div`
  // flex: 1;
  text-align: left;
  font-style: normal;
  font-weight: 700;
  font-size: 14px;
  line-height: 20px;
  color: #323334;
  margin-bottom: 7px;
`;

const Description = styled.div`
  font-style: normal;
  font-weight: 400;
  font-size: 18px;
  line-height: 28px;
`;

const AnonymizeActionButton = styled(Button)`
  border-radius: 30px !important;
  background-color: #0000e7 !important;
  color: white !important;
  // margin-right: 8px;
  border: 2px solid #0000e7 !important;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  padding: 12px 18px;
  background: #0000f0;
  border-radius: 100px;
  font-style: normal;
  font-size: 12px;
  line-height: 16px;
  letter-spacing: 0.5px;
  &:hover {
    filter: brightness(200%) !important;
  }
`;

const TestingImg = styled.img``;
const ActionButton = styled(Button)`
  box-sizing: border-box;
  padding: 12px 18px;
  border: 2px solid #003cff;
  border-radius: 100px !important;
  background-color: transparent !important;
  border: 2px solid #0000e7 !important;
  // margin-right: 8px;
  // margin-left: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-style: normal;
  font-size: 12px;
  line-height: 16px;
  letter-spacing: 0.5px;
  color: #003cff !important;
  &:hover {
    filter: brightness(200%) !important;
  }
`;

const ActionButtons = styled.div`
  display: flex;
  align-items: center;
  margin-top: 24px;
  flex-wrap: wrap;
  gap: 16px;
  ${(props) => props.showAnonymizedText && "display: none;"};
  @media (max-width: 385px) {
    margin-top: 16px;
  }
  @media (max-width: 987px) {
    ${(props) => props.showAnonymizedText === false && "display: none;"};
    ${(props) => props.showAnonymizedText === true && "display: flex;"};
  }
`;

const EntityTable = styled(Table)`
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
      td {
        padding: 10px 16px;
      }
    }
  }
`;

function Anonymizer() {
  const [showAnonymizedText, setShowAnonymizedText] = useState(false);
  const [editAnonymizedText, setEditAnonymizedText] = useState(false);
  const [inputText, setInputText] = useState("");
  const [outputText, setOutputText] = useState("");
  const [entityModalOpened, setEntityModalOpened] = useState(false);
  const [pseudonymisedWords, setPseudonymisedWords] = useState([]);
  const [entities, setEntities] = useState([]);
  const columns = [
    {
      dataIndex: "vaartus",
      key: "vaartus",
      title: "VAARTUS",
      width: 175,
      render(text, record, index) {
        return {
          children: (
            <Tag
              style={{
                padding: "5px 16px",
                color: pickTextColorBasedOnBgColorAdvanced(
                  record.color,
                  "#FFFFFF",
                  "#000000"
                ),
                fontWeight: "bold",
              }}
              color={record.color}
            >
              {text}
            </Tag>
          ),
        };
      },
    },
    {
      title: "KIRJELDUS",
      dataIndex: "kirjeldus",
      key: "kirjeldus",
      defaultSortOrder: "descend",
      sorter: (a, b) => a.kirjeldus.localeCompare(b.kirjeldus),
    },
  ];

  useEffect(() => {
    getEntities().then((x) =>
      setEntities(
        x.map((entity, index) => ({
          vaartus: entity.name,
          kirjeldus: entity.description,
          color: entityColors[index % entityColors.length],
        }))
      )
    );
  }, []);

  const downloadTxtFile = () => {
    const element = document.createElement("a");
    const file = new Blob([outputText], { type: "text/plain" });
    element.href = URL.createObjectURL(file);
    element.download = "output.txt";
    document.body.appendChild(element); // Required for this to work in FireFox
    element.click();
  };

  const getPseudonymiseText = async (e) => {
    setShowAnonymizedText(false);
    setOutputText("");
    setPseudonymisedWords([]);
    let response = await pseudonymiseText(inputText);
    setShowAnonymizedText(true);
    setOutputText(response?.[0]?.pseudonümiseeritud_tekst);
    let tagIndex = 0;
    response?.[0]?.Mapping.map((x) => {
      if (x.Tag !== "O" || x.regex_entity_tag) {
        x.tagIndex = tagIndex;
        tagIndex++;
      }
    });
    setPseudonymisedWords(response?.[0]?.Mapping);
  };

  return (
    <>
      <Modal
        maskStyle={{ background: "rgba(0, 0, 135, 0.75)" }}
        closeIcon={<img src={CloseIcon} />}
        width={679}
        close
        onCancel={() => setEntityModalOpened(false)}
        title={"Anonümiseerimise legend"}
        open={entityModalOpened}
        footer={
          <ThemeButton onClick={() => setEntityModalOpened(false)}>
            SULGE
          </ThemeButton>
        }
      >
        <EntityTable
          scroll={{
            y: 300,
          }}
          pagination={false}
          dataSource={entities}
          columns={columns}
        />
      </Modal>
      <Container>
        <Title>anonüümi teksti</Title>
        <Description>
          Rakendus töötab vaid eestikeelsete tekstidega. Tähemärgipiirang kuni
          500 sümbolit koos tühikutega
        </Description>
        <AnonymizerTextContainer>
          <AnonymizerTextCardContainer>
            <div>
              <InputHeading>Sisend</InputHeading>
              {showAnonymizedText && !editAnonymizedText ? (
                <AnonymizerTextCard
                  onClick={() => {
                    setEditAnonymizedText(true);
                  }}
                >
                  {pseudonymisedWords.map((x) =>
                    x.Tag === "O" && !x.regex_entity_tag ? (
                      <div>{x.Algne}&nbsp;</div>
                    ) : (
                      <>
                        <KeywordTag
                          color={tagColors[x.tagIndex % tagColors.length]}
                          text={x.Algne}
                          keyword={x.regex_entity_tag ? x.regex_entity_tag : x.Tag?.split("_")?.[0]}
                        />
                        &nbsp;
                      </>
                    )
                  )}
                </AnonymizerTextCard>
              ) : (
                <AnonymizerTextArea
                  autoFocus
                  onBlur={() => {
                    if (editAnonymizedText) setEditAnonymizedText(false);
                  }}
                  onFocus={(e) =>
                    e.currentTarget.setSelectionRange(
                      e.currentTarget.value.length,
                      e.currentTarget.value.length
                    )
                  }
                  onChange={(ev) => setInputText(ev.target.value)}
                  value={inputText}
                  placeholder={"Sisesta sila"}
                  rows={10}
                  maxLength={500}
                />
              )}
              <AnonymizerTextCount>
                {500 - inputText.length} tähemärki jäänud
              </AnonymizerTextCount>
            </div>
            <ActionButtons
              showAnonymizedText={
                showAnonymizedText === false ? showAnonymizedText : null
              }
            >
              <AnonymizeActionButton
                onMouseDown={getPseudonymiseText}
                size={"large"}
              >
                ANONÜMISEERI TEKST
              </AnonymizeActionButton>
              <ActionButton
                onClick={() => setEntityModalOpened(true)}
                size={"large"}
              >
                VAATA LEGENDI
              </ActionButton>
            </ActionButtons>
          </AnonymizerTextCardContainer>
          <AnonymizerTextAreaGap>
            <img src={RightIcon} />
          </AnonymizerTextAreaGap>
          <AnonymizerTextCardContainer>
            <div>
              <InputHeading>Väljund</InputHeading>
              <AnonymizerTextCard
                isEditing={!(showAnonymizedText && !editAnonymizedText)}
              >
                {outputText}
              </AnonymizerTextCard>
            </div>
            {showAnonymizedText ? (
              <ActionButtons>
                <ActionButton onClick={downloadTxtFile} size={"large"}>
                  LAE ALLA .TXT FALINA
                </ActionButton>
                <ActionButton
                  onClick={() => {
                    navigator.clipboard.writeText(outputText);
                    notification.info({
                      description: "Anonüümitud tekst kopeeritud",
                      placement: "bottomLeft",
                      icon: <div />,
                      closeIcon: <div />,
                    });
                  }}
                  size={"large"}
                >
                  KOPEERI VÄLJUNDTEKST
                </ActionButton>
              </ActionButtons>
            ) : (
              <ActionButtons showAnonymizedText={!showAnonymizedText}>
                <AnonymizeActionButton
                  onMouseDown={getPseudonymiseText}
                  size={"large"}
                >
                  ANONÜMISEERI TEKST
                </AnonymizeActionButton>
                <ActionButton
                  onClick={() => setEntityModalOpened(true)}
                  size={"large"}
                >
                  VAATA LEGENDI
                </ActionButton>
              </ActionButtons>
            )}
          </AnonymizerTextCardContainer>
        </AnonymizerTextContainer>
      </Container>
      <GithubSection />
    </>
  );
}

export default Anonymizer;
