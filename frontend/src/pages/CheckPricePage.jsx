import React, { useState, useEffect } from 'react';
import { authApi } from '../api/axios';
import { TrendingUp, Package, AlertCircle } from 'lucide-react';

const CheckPricePage = () => {
    const [prices, setPrices] = useState([]);
    const [loading, setLoading]= useState(true);

    useEffect(() => {
        const fetchPrices = async () => {
            try{
                const res = await authApi.get('/prices/latest-summary');
                setPrices(res.data);
                console.log(res.data);
            } catch (err) {
                console.error("Fetch error", err);
            } finally {
                setLoading(false);
            }
        };
        fetchPrices();
    }, []);

    const getStatusBadge = (avg, latest) => {
        if (!avg || !latest) return null;
        const diff = ((latest - avg) / avg) * 100;
        if (diff <= -5) return <span className="px-2 py-1 bg-green-100 text-green-600 text-[9px] font-black rounded-md">🟢 GOOD DEAL</span>;
        if (diff >= 5) return <span className="px-2 py-1 bg-red-100 text-red-600 text-[9px] font-black rounded-md">🔴 OVERPRICED</span>;
        return <span className="px-2 py-1 bg-slate-200 text-blue-500 text-[9px] font-black rounded-md flex items-center gap-1 shadow-sm">⚪️ STABLE</span>;
    }

    if (loading) return <div className="py-20 text-center text-gray-400 text-sm animate-pulse">Fetching your latest data...</div>;

    return (
        <div className="space-y-3 max-h-[400px] overflow-y-auto pr-2 custom-scrollbar animate-in fade-in">
            {prices.length === 0 ? (
                <div className="text-center py-10 text-gray-400 text-sm">No historical data available.</div>
            ) : (
                prices.map((item, index) => (
                    <div key={index} className="flex justify-between items-center p-5 bg-slate-50 rounded-2xl border border-slate-100 hover:border-slate-200 transition-all">
                        <div className="flex items-center gap-3">
                            <div className="p-2 bg-white rounded-lg shadow-sm text-slate-400"><Package size={18}/></div>
                            <div>
                                <div className="text-sm font-bold text-slate-800">{item.product_name}</div>
                                <div className="text-[10px] text-slate-400 uppercase font-medium">
                                     Avg of Latest 4 Prices: <span className="text-slate-600">${item.average_price}</span>
                                </div>
                                
                            </div>
                        </div>
                        <div className="text-right flex flex-col items-end gap-1">
                            {getStatusBadge(item.average_price, item.latest_price)}
                            <div className="text-lg font-black text-black">${item.latest_price}</div>
                            <div className="text-[9px] font-bold text-green-500 flex items-center justify-end uppercase tracking-tighter">
                                <TrendingUp size={10} className="mr-1"/> Latest Price
                            </div>
                        </div>
                    </div>
                ))
            )}
        </div>
    );
};

export default CheckPricePage;