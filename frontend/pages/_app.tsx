import 'bootstrap/dist/css/bootstrap.min.css';

function MyApp({ Component, pageProps }) {
  return (
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
  );
}

export default MyApp;
