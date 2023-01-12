import styled from "styled-components";
import { useLocation, Link } from "react-router-dom";
import { useState } from "react";
import DrawerIcon from "../assets/Drawer.svg";
import Drawer from "./Drawer";
import { useState } from "react";

const Container = styled.div`
  background: #0000e6;
  width: 100%;
  padding: 25px 32px;
  color: white;
  display: flex;
  justify-content: space-between;
  position: sticky;
  top: 0;
  left: 0;
  z-index: 999;
  @media (max-width: 680px) {
    padding: 25px 16px;
  }
`;

const Heading = styled.div`
  font-style: normal;
  font-weight: 700;
  font-size: 18px;
  line-height: 28px;
  color: #ffffff;
`;

const NavigationItems = styled.div`
  display: flex;
  @media (max-width: 925px) {
    display: none;
  }
`;

const NavigationItemsDrawerToggle = styled.img`
  width: 16px;
  height: 28px;
  display: flex;
  cursor: pointer;
  margin-right: 5px;
  // padding: 16px;
  @media (min-width: 925px) {
    display: none;
  }
`;

const NavigationItem = styled(Link)`
  margin-right: 72px;
  border-bottom: ${(props) => props.selected && "1px solid"};
  height: 22px;
  font-style: normal;
  font-weight: 400;
  font-size: 20px;
  line-height: 23px;
  color: #ffffff;
`;

const VerticalLine = styled.div`
  border-left: 3px white solid;
  margin-right: 72px;
`;

const EnglishText = styled.div`
  font-style: normal;
  font-weight: 400;
  font-size: 18px;
  line-height: 28px;
  color: #ffffff;
`;

function Header() {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const location = useLocation();
  const [drawerOpen, setDrawerOpen] = useState(false);
  return (
    <>
      <Drawer drawerOpen={drawerOpen} setDrawerOpen={setDrawerOpen} />
      <Container>
        <Heading drawerOpen={drawerOpen} setDrawerOpen={setDrawerOpen}>
          bürokrati anonüümija
        </Heading>
        <NavigationItems>
          <NavigationItem to={"/"} selected={location.pathname === "/"}>
            Anonüümija
          </NavigationItem>
          <NavigationItem
            to={"/treening"}
            selected={location.pathname === "/treening"}
          >
            Treenija
          </NavigationItem>
          <NavigationItem style={{ marginRight: 10 }}>Github</NavigationItem>
        </NavigationItems>
        <NavigationItemsDrawerToggle
          onClick={() => setDrawerOpen(true)}
          src={DrawerIcon}
        />
      </Container>
    </>
  );
}

export default Header;
