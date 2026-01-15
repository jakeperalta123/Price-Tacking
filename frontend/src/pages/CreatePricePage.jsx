import React, { useState } from 'react';
import { Package, DollarSign, Ruler, Tag, Store } from 'lucide-react';
import { authApi } from '../api/axios';
import InputField from '../components/InputField';

const CreatePricePage = ({onSuccess}) => {
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        name: '', unit: '', price: '', store: '', category: ''
    });

    const handleCreateProduct = async (e) => {
        e.preventDefault();
        setLoading(true);
        try{
            await authApi.post('/products/price', formData);
            alert("Product and Price created successfully!");
            setFormData({ name: '', unit: '', price: '', store: '', category: ''});
            if (onSuccess) onSuccess();
        } catch(error){
            alert(error.response?.data?.detail || "Action Failed");
        } finally{
            setLoading(false)
        }
    };

    return (
        <form onSubmit={handleCreateProduct} className="space-y-4 animate-in fade-in duration-500">
            <InputField 
                label="Product Name" icon={Package} placeholder="e.g. Model 3 Tire"
                value={formData.name} onChange={(val) => setFormData({...formData, name: val})}
            />
            <div className="grid grid-cols-2 gap-4">
                <InputField 
                    label="Price (USD)" icon={DollarSign} type="number" placeholder="0.00"
                    value={formData.price} onChange={(val) => setFormData({...formData, price: val})}
                />
                <InputField 
                    label="Unit" icon={Ruler} placeholder="e.g. Piece"
                    value={formData.unit} onChange={(val) => setFormData({...formData, unit: val})}
                />
            </div>
            <InputField 
                label="Store" icon={Store} placeholder="Optional"
                value={formData.store} onChange={(val) => setFormData({...formData, store: val})}
            />
            <InputField 
                label="Category" icon={Tag} placeholder="Optional"
                value={formData.category} onChange={(val) => setFormData({...formData, category: val})}
            />

            <button 
                type="submit" disabled={loading}
                className="w-full bg-black text-white py-4 rounded-xl font-bold text-xs tracking-[0.2em] uppercase mt-4 hover:bg-gray-800 disabled:bg-gray-400 transition-all"
            >
                {loading ? "Processing..." : "Confirm & Save"}
            </button>
        </form>
    );
};

export default CreatePricePage;