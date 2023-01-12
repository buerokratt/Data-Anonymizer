import styled from "styled-components";

const Container = styled.div`
  background: #000090;
  width: 100%;
  padding: 24px 16px;
  color: white;
  display: flex;
  justify-content: center;
  min-height: 79px;
  align-items: center;
`;

const Heading = styled.div`
  font-style: normal;
  font-weight: 400;
  font-size: 18px;
  line-height: 28px;
  text-align: center;
`;

const GihubLink = styled.a`
  text-decoration: underline;
  color: white;
`;

function GithubSection() {
  return (
    <Container>
      <Heading>
        Täisfunktsionaalse rakenduse kasutamiseks lae endale alla täisversioon
        meie <GihubLink>Githubi repositooriumist</GihubLink>.
      </Heading>
    </Container>
  );
}

export default GithubSection;
