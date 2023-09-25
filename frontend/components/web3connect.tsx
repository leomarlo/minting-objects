// src/Web3ModalComponent.js

import React, { useState, useEffect } from 'react';
import Web3 from 'web3';
import Web3Modal from 'web3modal';
import WalletConnectProvider from '@walletconnect/web3-provider';

const providerOptions = {
  walletconnect: {
    package: WalletConnectProvider,
    options: {
      infuraId: "YOUR_INFURA_ID"  // Replace with your Infura ID
    }
  }
};



function Web3ModalComponent() {
  const [account, setAccount] = useState<null | string>(null);
  const [web3Modal, setWeb3Modal] = useState<null | Web3Modal>(null) 

  useEffect(() => {
    let web3ModalTemp : Web3Modal | null = null
    if (web3Modal===null) {
      let web3Modal = new Web3Modal({
        network: "mainnet",
        cacheProvider: true,
        providerOptions
      });
      setWeb3Modal(web3Modal);
      web3ModalTemp = web3Modal;
    }

    if (web3ModalTemp!==null){
      // it means that web3Modal is not null
      if ((web3ModalTemp as Web3Modal).cachedProvider) {
        onConnect();
      }
    }
    
  }, []);


  

  const onConnect = async () => {
    const provider = await (web3Modal as Web3Modal).connect();
    const web3 = new Web3(provider);
    const accounts = await web3.eth.getAccounts();
    setAccount(accounts[0]);
    provider.on("accountsChanged", (accounts: Array<string>) => {
      setAccount(accounts[0]);
    });
  };

  return (
    <div>
      {account ? (
        <div>Connected: {account}</div>
      ) : (
        <button className="btn btn-success" onClick={onConnect}>Connect Wallet</button>
      )}
    </div>
  );
}


interface CustomizedWeb3ModalProps {
  buttonText: string;
  classNames: string;
  callbackFunction: any;
  setterOfEthAccount: any
}

const Web3ModalCustomized: React.FC<CustomizedWeb3ModalProps> = ({ buttonText, classNames, callbackFunction, setterOfEthAccount }) => {
  const [account, setAccount] = useState<null | string>(null);
  const [web3Modal, setWeb3Modal] = useState<null | Web3Modal>(null) 

  useEffect(() => {
    let web3ModalTemp : Web3Modal | null = null
    if (web3Modal===null) {
      let web3Modal = new Web3Modal({
        network: "mainnet",
        cacheProvider: true,
        providerOptions
      });
      setWeb3Modal(web3Modal);
      web3ModalTemp = web3Modal;
    }

    if (web3ModalTemp!==null){
      // it means that web3Modal is not null
      if ((web3ModalTemp as Web3Modal).cachedProvider) {
        onConnect();
      }
    }
    
  }, []);

  const onConnect = async () => {
    const provider = await (web3Modal as Web3Modal).connect();
    const web3 = new Web3(provider);
    const accounts = await web3.eth.getAccounts();
    setAccount(accounts[0]);
    setterOfEthAccount(accounts[0])
    provider.on("accountsChanged", (accounts: Array<string>) => {
      setAccount(accounts[0]);
      setterOfEthAccount(accounts[0]);
    });
  };

  const handleConnectButton = async ()=> {
    await onConnect();
    await callbackFunction();
  }

  return (
    <div>
      <button className={classNames} onClick={handleConnectButton}>{buttonText}</button>
    </div>
  );
}


export {
  Web3ModalComponent,
  Web3ModalCustomized
};
