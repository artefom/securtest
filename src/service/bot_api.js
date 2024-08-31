import Axios from 'axios';

const baseURL = '';

const axiosInstance = Axios.create({ baseURL, withCredentials: true, timeout: 2500 });

/**
 * single tone api function
 * @returns axios instance
 */
const request = () => axiosInstance;

const url = import.meta.env.VITE_BOT_API;

export default {
  record_result_stats: () => {
    return request().post(`${url}/record-result-stats`);
  },
};
