import {
  Button,
  Classes,
  Navbar,
  NavbarDivider,
  NavbarGroup,
  NavbarHeading,
} from "@blueprintjs/core";

export default function AppNavbar() {
  return (
    <Navbar>
      <NavbarGroup>
        <NavbarHeading>Reporter</NavbarHeading>
        <NavbarDivider />
        <Button className={Classes.MINIMAL} icon="home" text="Home" />
        <Button className={Classes.MINIMAL} icon="document" text="Files" />
      </NavbarGroup>
    </Navbar>
  );
}
