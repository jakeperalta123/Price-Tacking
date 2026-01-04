import axios from 'axios';

export const publicApi = axios.create({
    baseURL: 'http://127.0.0.1:8000',
});

export const authApi = axios.create({
    baseURL: 'http://127.0.0.1:8000',
})

authApi.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
})



