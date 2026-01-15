import React, { useState } from 'react';
import CreatePricePage from './CreatePricePage';
import CheckPricePage from './CheckPricePage';

const ProductManager = ({ initialTab = 'create', onClose }) => {
    const [activeTab, setActiveTab] = useState(initialTab);

    return (
        <div className="relative bg-white w-full max-w-[500px] rounded-[35px] p-10 shadow-2xl animate-in zoom-in-95 duration-200">
            <div className="flex bg-slate-100 p-1 rounded-2xl mb-8">
                <button 
                    onClick={() => setActiveTab('create')}
                    className={`flex-1 py-3 rounded-xl text-xs font-black uppercase tracking-widest transition-all ${activeTab === 'create' ? 'bg-white shadow-sm text-black' : 'text-slate-400'}`}
                >
                    Create Price
                </button>
                <button 
                    onClick={() => setActiveTab('check')}
                    className={`flex-1 py-3 rounded-xl text-xs font-black uppercase tracking-widest transition-all ${activeTab === 'check' ? 'bg-white shadow-sm text-black' : 'text-slate-400'}`}
                >
                    Check Price
                </button>
            </div>

            {activeTab === 'create' ? (
                <CreatePricePage onSuccess={() => setActiveTab('check')} />
            ) : (
                <CheckPricePage />
            )}

            <button 
                onClick={onClose}
                className="mt-6 w-full py-2 text-slate-400 text-[10px] font-bold tracking-widest uppercase hover:text-black transition-all"
            >
                Dismiss
            </button>
        </div>
    );
};

export default ProductManager;