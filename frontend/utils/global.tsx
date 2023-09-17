
let DEVELOPMENT_MODE: string = process.env.REACT_APP_DEVELOPMENT_MODE || 'development';
let DOCKER_MODE: boolean = process.env.REACT_APP_DOCKERIZED === 'dockerized' || false;
let REVERSE_PROXY: boolean = DOCKER_MODE;

const BACKEND_URL = REVERSE_PROXY ? '/api/' : 'http://localhost:5000/';

const MIN_UPLOADS_PER_OBJECT = DEVELOPMENT_MODE=='local' ? 1 : 6;

console.log('DEVELOPMENT_MODE', DEVELOPMENT_MODE)
console.log('process.env.REACT_APP_DEVELOPMENT_MODE ', process.env.REACT_APP_DEVELOPMENT_MODE )

const MAIN_PRODUCT_IDS = ['schmiede23','blood']
const TEST_PRODUCT_IDS = ['veggies']
const DEV_PRODUCT_IDS = ['socks']
const PRODUCT_IDS = DEVELOPMENT_MODE=='local' ? TEST_PRODUCT_IDS : (DEVELOPMENT_MODE=='production' ? MAIN_PRODUCT_IDS: DEV_PRODUCT_IDS)


export { DEVELOPMENT_MODE, REVERSE_PROXY, DOCKER_MODE, BACKEND_URL, MIN_UPLOADS_PER_OBJECT, PRODUCT_IDS };
