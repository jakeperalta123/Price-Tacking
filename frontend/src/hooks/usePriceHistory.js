import { useState, useEffect } from 'react';
import { authApi } from '../api/axios';

export const usePriceHistory = (productId) => {
    const [data, setData] = useState([]);
    const[loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchHistory = async () => {
            if (!productId) return;
            try {
                setLoading(true);
                const res = await authApi.get(`/prices/history/${productId}`);
                const formatted = res.data.map(item => {
                    const dateObj = new Date(item.created_at);
                    return {
                        ...item,
                        price: item.price !== null ? parseFloat(item.price) : null,
                        time: dateObj.toLocaleDateString('zh-TW', { 
                            month: '2-digit', 
                            day: '2-digit' 
                        }),
                        fullDate: dateObj.toLocaleString('zh-TW', {
                            year: 'numeric',
                            month: '2-digit',
                            day: '2-digit',
                            hour: '2-digit',
                            minute: '2-digit',
                            second: '2-digit',
                            hour12: false
                        })
                    };
                });
                setData(formatted);
            } catch (err) {
                console.error("failed to fetch history price: ", err);
            } finally {
                setLoading(false);
            }
        };
        fetchHistory();
    }, [productId]);
    return {data, loading};
}

