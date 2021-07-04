import { CSRF_TOKEN } from "./csrf_token.js"

import axios from 'axios';

export const HTTP = axios.create({
  baseURL: `http://127.0.0.1:8000/api/`,
  headers: {
    'content-type': 'application/json',
    'X-CSRFTOKEN': CSRF_TOKEN
  }
})
