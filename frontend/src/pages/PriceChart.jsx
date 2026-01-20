import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { usePriceHistory } from '../hooks/usePriceHistory';

const PriceChart = ({ productId }) => {
    const { data, loading } = usePriceHistory(productId);

    if (loading) return (
        <div className="h-48 w-full flex items-center justify-center text-slate-400 text-xs animate-pulse font-medium">
            GENERATING PRICE TRENDS...
        </div>
    );

    return (
        <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                    <defs>
                        <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                            <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                        </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                    <XAxis dataKey="time" fontSize={9} tickLine={false} axisLine={false} tick={{ fill: '#94a3b8' }} interval={1} padding={{ left: 10, right: 10 }} />
                    <YAxis fontSize={10} tickLine={false} axisLine={false} tick={{fill: '#94a3b8'}} domain={['auto', 'auto']} />
                    // 在 AreaChart 組件中修改 Tooltip 部分
                    <Tooltip 
                        labelFormatter={(label, payload) => {
                            return payload[0]?.payload?.fullDate || label;
                        }}
                        contentStyle={{ 
                            borderRadius: '12px', 
                            border: 'none', 
                            boxShadow: '0 10px 15px -3px rgba(0,0,0,0.1)',
                            fontSize: '12px' 
                        }}
                        formatter={(value) => [`$${value}`, "Price"]}
                    />
                    <Area 
                        type="monotone" 
                        dataKey="price" 
                        stroke="#3b82f6" 
                        strokeWidth={3}
                        fillOpacity={1} 
                        fill="url(#colorPrice)" 
                        connectNulls={false}
                        dot={{ r: 4, fill: '#3b82f6', strokeWidth: 2, stroke: '#fff' }}
                    />
                </AreaChart>
            </ResponsiveContainer>
        </div>
    )
}

export default PriceChart;