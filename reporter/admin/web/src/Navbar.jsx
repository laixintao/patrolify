import {
  Button,
  Classes,
  Navbar,
  NavbarDivider,
  NavbarGroup,
  NavbarHeading,
} from "@blueprintjs/core";
import { Link } from "react-router-dom";

export default function AppNavbar() {
  return (
    <Navbar>
      <NavbarGroup>
        <NavbarHeading>Reporter</NavbarHeading>
        <NavbarDivider />
        <Link to="/">
          <Button className={Classes.MINIMAL} icon="home" text="Home" />
        </Link>
        <Button className={Classes.MINIMAL} icon="document" text="Files" />
      </NavbarGroup>
    </Navbar>
  );
}
