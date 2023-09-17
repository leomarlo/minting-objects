
let DEVELOPMENT_MODE: string = process.env.REACT_APP_DEVELOPMENT_MODE || 'development';
let DOCKER_MODE: boolean = process.env.REACT_APP_DOCKERIZED === 'dockerized' || false;
let REVERSE_PROXY: boolean = DOCKER_MODE;

const BACKEND_URL = REVERSE_PROXY ? '/api/' : 'http://localhost:5000/';

const MIN_UPLOADS_PER_OBJECT = DEVELOPMENT_MODE=='local' ? 1 : 6;

const MAIN_PRODUCT_ID = 'schmiede'
const TEST_PRODUCT_ID = 'veggies'
const DEV_PRODUCT_ID = 'socks'
const PRODUCT_ID = DEVELOPMENT_MODE=='local' ? TEST_PRODUCT_ID : (DEVELOPMENT_MODE=='production' ? MAIN_PRODUCT_ID: DEV_PRODUCT_ID)


export { DEVELOPMENT_MODE, REVERSE_PROXY, DOCKER_MODE, BACKEND_URL, MIN_UPLOADS_PER_OBJECT, PRODUCT_ID };
