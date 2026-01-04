import React, {useState}  from "react";
import {Eye, EyeOff} from 'lucide-react';
import { publicApi} from "../api/axios";
import { useNavigate } from "react-router-dom";

function UserRegister() {
    
    const [regEmail, setRegEmail] = useState('');
    const [regUsername, setRegUsername] = useState('');
    const [regPassword, setRegPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const navigate = useNavigate();
    const handleRegistger = async (e) => {
        e.preventDefault();
        

        const currentEmail = regEmail.trim();
        if (!currentEmail.includes('@')){
            alert("Error in email format, need to include @");
            return;
        }

        const userData = {
            email: regEmail, 
            username: regUsername, 
            password: regPassword
        };

        try{
            const response = await publicApi.post('/users/register', userData);
            console.log("Successfully Registerd! Backend sends: ", response.data);
            alert(`註冊成功！歡迎 ${response.data.username || regUsername}`);
            navigate('/login');
        } catch(error){
            console.error("failed", error);
            const errorMsg = error.response?.data?.detail || "伺服器沒有回應，請檢查後端是否啟動";
            alert("註冊失敗：" + errorMsg);
        }
    };
    return (
        <div className="p-10">
            <h2>Register</h2>
            <form onSubmit={handleRegistger} className="space-y-4">
                <div>
                    <input
                        className="border p-2 w-full"
                        placeholder="Email"
                        value={regEmail}
                        onChange={(e) => setRegEmail(e.target.value)}
                    />
                </div>
                <div>
                    <input
                        className="border p-2 w-full"
                        placeholder="UserName"
                        value={regUsername}
                        onChange={(e) => setRegUsername(e.target.value)}
                    />
                </div>
                <div className="relative">
                    <input
                        type={showPassword ? "text": "password"}
                        className="border p-2 w-full"
                        placeholder="Password"
                        value={regPassword}
                        onChange={(e) => setRegPassword(e.target.value)}
                    />
                    <button 
                        type="button" 
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-2 top-2 text-gray-500"
                    >
                        {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                    </button>
                </div>
                <button 
                    type="submit" 
                    className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
                >
                    Register Now
                </button>
            </form>
            
        </div>
    )
}

export default UserRegister;