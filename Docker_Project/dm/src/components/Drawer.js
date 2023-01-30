import styled from "styled-components";
import { useLocation, Link } from "react-router-dom";
import { useState } from "react";
import CloseIcon from "../assets/close_white.svg";
import { useTranslation } from "react-i18next";

const Container = styled.div`
  visibility: ${(props) => (props.drawerOpen ? "visible" : "hidden")};
  overflow: hidden;
  transition: all 1s ease;
  background: #0000e6;
  width: 100%;
  position: absolute;
  z-index: 9999999999999;
  bottom: ${(props) => (props.drawerOpen ? "0px" : "100%")};
  top: 0px;
  left: 0px;
  right: 0px;
  // bottom: 0px;
  padding: 25px 32px;
  @media (max-width: 680px) {
    padding: 25px 16px;
  }
`;

const DrawerHeaderRow = styled.div`
  display: flex;
  justify-content: space-between;
  height 54px;
  margin-bottom: 24px;
`;

const DrawerRow = styled.div`
  display: flex;
  padding: 12px 0px;
  margin-bottom: 8px;
`;

const Heading = styled.div`
  font-style: normal;
  font-weight: 700;
  font-size: 18px;
  line-height: 28px;
  color: #ffffff;
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

function Drawer({ drawerOpen, setDrawerOpen }) {
  const location = useLocation();
  const { t } = useTranslation("common");
  return (
    <Container drawerOpen={drawerOpen}>
      <DrawerHeaderRow>
        <Heading>{t("header.title")}</Heading>
        <NavigationItemsDrawerToggle
          onClick={() => setDrawerOpen(false)}
          src={CloseIcon}
        />
      </DrawerHeaderRow>
      <DrawerRow>
        <NavigationItem
          onClick={() => setDrawerOpen(false)}
          to={"/"}
          selected={location.pathname === "/"}
        >
          {t("header.anonymizer")}
        </NavigationItem>
      </DrawerRow>
      <DrawerRow>
        <NavigationItem
          onClick={() => setDrawerOpen(false)}
          to={"/treening"}
          selected={location.pathname === "/treening"}
        >
          {t("header.training")}
        </NavigationItem>
      </DrawerRow>
      <DrawerRow>
        <NavigationItem to="#" onClick={() => setDrawerOpen(false)}>
          {t("header.github")}
        </NavigationItem>
      </DrawerRow>
    </Container>
  );
}

export default Drawer;
