import React from 'react';

const InputField = ({icon: Icon, label, type="text", value, onChange, placeholder}) => (
    <div className="space-y-1">
        <label className="text-sm font-bold text-slate-700 ml-1">
            {label}
        </label>
        <div className="relative">
            {Icon &&(
                <Icon
                    className="absolute left-3 top-3 text-slate-400" 
                    size={18}
                />
            )}

            <input
                type={type}
                value={value}
                onChange={(e) => onChange(e.target.value)}
                placeholder={placeholder}
                className="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition-all"
            />
        </div>
    </div>
);

export default InputField;