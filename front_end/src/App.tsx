import React from 'react';
import logo from './logo.svg';
import { DAppProvider, Mainnet, Config, ChainId, Kovan } from '@usedapp/core';
import { getDefaultProvider } from 'ethers'
import { Header } from './components/Header';
import {Container} from "@material-ui/core"
import { Main } from './components/Main';

const config: Config = {
  readOnlyChainId: Kovan.chainId,
  readOnlyUrls: {
    [Kovan.chainId]: getDefaultProvider('kovan'),
  },
  notifications: {
    expirationPeriod: 1000,
    checkInterval: 1000
  }
}

function App() {
  return (
    <DAppProvider config={config}>
      <Header></Header>
      <Container maxWidth="md">
        <div>Hi</div>
        <Main></Main>
      </Container>
    </DAppProvider>
  );
}

export default App;
