import React from "react";
import { render } from 'react-dom';
import { ThemeProvider } from "@chakra-ui/core";

import Header from "./Components/Header";
import Todos from "./Components/Todos";

const { initialize } = require('@heliosphere/web-sdk');

initialize({
    apiToken: 'a9665ac9688fe681e2d1',
    serviceName: 'frontend',
    enable: true,
    environment: 'local_aviv'
});


function App() {
  return (
    <ThemeProvider>
      <Header />
      <Todos />
    </ThemeProvider>
  )
}

const rootElement = document.getElementById("root")
render(<App />, rootElement)
