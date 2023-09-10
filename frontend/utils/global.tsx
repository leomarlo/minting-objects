
let DEVELOPMENT_MODE: string = process.env.REACT_APP_DEVELOPMENT_MODE || 'development';
let DOCKER_MODE: boolean = process.env.REACT_APP_DOCKERIZED === 'dockerized' || false;
let REVERSE_PROXY: boolean = DOCKER_MODE;

const BACKEND_URL = REVERSE_PROXY ? '/api/' : 'http://localhost:5000/';

export { DEVELOPMENT_MODE, REVERSE_PROXY, DOCKER_MODE, BACKEND_URL };
