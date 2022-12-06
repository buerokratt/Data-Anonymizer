import styled from "styled-components";
import Authority1 from "../assets/Est_Authority_1.svg";
import Authority2 from "../assets/Est_Authority_2.svg";
import Authority3 from "../assets/Est_Authority_3.svg";

const Container = styled.div`
  width: 100%;
  color: white;
  display: flex;
  justify-content: center;
  padding: 30px;
  flex-wrap: wrap;
  @media (max-width: 366px) {
    padding: 24px 16px;
  }
  @media (max-width: 680px) {
    gap: 16px;
  }
`;

const Image1 = styled.img`
  margin-right: 72px;
  @media (max-width: 680px) {
    margin-right: 0px;
  }
  @media (max-width: 458px) {
    width: 165px;
    height: 72px;
  }
`;

const Image2 = styled.img`
  margin-right: 72px;
  @media (max-width: 680px) {
    margin-right: 0px;
  }
  @media (max-width: 458px) {
    width: 141;
    height: 72px;
  }
`;

const Image3 = styled.img`
  @media (max-width: 458px) {
    width: 125;
    height: 72px;
  }
`;

function Footer() {
  return (
    <Container>
      <Image1 src={Authority1} />
      <Image2 src={Authority2} />
      <Image3 src={Authority3} />
    </Container>
  );
}

export default Footer;
