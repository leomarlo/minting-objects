import { AppProps } from 'next/app';
import { Web3ModalProvider } from '../contexts/web3Context';
import 'bootstrap/dist/css/bootstrap.min.css';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <Web3ModalProvider>
    <div>
      <header>
        {/* You can put a navigation bar here */}
      </header>
      
      {/* This renders the current page */}
      <Component {...pageProps} />
      
      <footer>
        {/* You can put a footer here */}
      </footer>
    </div>
    </Web3ModalProvider>
  );
}

export default MyApp;
