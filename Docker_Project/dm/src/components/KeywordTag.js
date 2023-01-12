import styled from "styled-components";
import { Tag } from "antd";

const ParentTag = styled(Tag)`
  padding: 0px 6px;
  background: #a0e432;
  border-radius: 4px;
  color: black;
  font-size: 12px;
  margin-right: 4px;
  margin-bottom: 4px;
  font-style: normal;
  font-weight: 400;
  font-size: 16px;
  line-height: 24px;
  display: flex;
  align-items: center;
`;

const ChildTag = styled(Tag)`
  font-weight: bold;
  font-size: 10px;
  height: 20px;
  margin: 0px;
  border-radius: 4px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 5px 4px 4px;
  background: #ffffff;
  font-style: normal;
  font-size: 8px;
  line-height: 8px;
  margin-left: 4px;
`;

function KeywordTag({ color, text, keyword }) {
  return (
    <ParentTag color={color}>
      {text} <ChildTag>{keyword}</ChildTag>
    </ParentTag>
  );
}

export default KeywordTag;
