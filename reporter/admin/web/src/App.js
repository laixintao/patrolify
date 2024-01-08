import {
  Alignment,
  Button,
  FocusStyleManager,
  Navbar,
} from "@blueprintjs/core";
import "./App.css";

FocusStyleManager.onlyShowFocusOnTabs();

function App() {
  return (
    <div className="App">
      <Navbar>
        <Navbar.Group align={Alignment.LEFT}>
          <Navbar.Heading>Reporter</Navbar.Heading>
          <Navbar.Divider />
          <Button className="bp5-minimal" icon="home" text="Home" />
          <Button className="bp5-minimal" icon="document" text="Files" />
        </Navbar.Group>
      </Navbar>
    </div>
  );
}

export default App;
