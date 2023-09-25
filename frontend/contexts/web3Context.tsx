// contexts/Web3ModalContext.tsx

import { createContext, useContext, ReactNode, useState, useEffect } from 'react';
import Web3 from 'web3';
import Web3Modal from 'web3modal';

interface Web3ModalContextProps {
  web3?: Web3;
  account?: string;
  connect: () => void;
  disconnect: () => void;
}

const Web3ModalContext = createContext<Web3ModalContextProps | undefined>(undefined);

export const useWeb3Modal = () => {
  const context = useContext(Web3ModalContext);
  if (!context) {
    throw new Error('useWeb3Modal must be used within a Web3ModalProvider');
  }
  return context;
};

export const Web3ModalProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [web3, setWeb3] = useState<Web3 | undefined>();
  const [web3Modal, setWeb3Modal] = useState<any | null>(null);  // You can replace 'any' with the appropriate type if known
  const [account, setAccount] = useState<string | undefined>();

  useEffect(() => {
    const web3ModalInstance = new Web3Modal({
      network: "mainnet",
      cacheProvider: true,
      // Add other configurations if needed
    });
    setWeb3Modal(web3ModalInstance);
  }, []);
  const connect = async () => {
    if (web3Modal) {
      const provider = await web3Modal.connect();
      const web3Instance = new Web3(provider);
      setWeb3(web3Instance);
  
      // Get accounts
      const accounts = await web3Instance.eth.getAccounts();
      if (accounts.length > 0) {
        setAccount(accounts[0]);
      }
  
      // Optionally, you can listen for account changes
      provider.on("accountsChanged", (accounts: string[]) => {
        if (accounts.length === 0) {
          disconnect();  // Disconnect if no accounts are available
        } else {
          setAccount(accounts[0]);
        }
      });
    }
  };

  const disconnect = async () => {
    if (web3Modal && web3Modal.cachedProvider) {
      await web3Modal.clearCachedProvider();
      setWeb3(undefined);
      // Handle other logic after disconnecting if needed
    }
  };


  return (
    <Web3ModalContext.Provider value={{ web3, account, connect, disconnect }}>
      {children}
    </Web3ModalContext.Provider>
  );
};
