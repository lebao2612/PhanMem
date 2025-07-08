import { useState } from "react";
import { handlePressMenu } from "../scripts/home";
import images from "../assets/images";
import { useNavigate } from "react-router-dom";

const LeftSideBar = () =>{
    const navigate = useNavigate();
    const [menuOpen, setMenuOpen] = useState(false);
    return (
        <div className="border-1 border-zinc-800">
            {/* Overlay */}
            {menuOpen && (
            <div
                className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
                onClick={handlePressMenu(menuOpen, setMenuOpen)}
            ></div>
            )}
    
            {/* Left Sidebar */}
            <div className={`w-16 border-r border-zinc-800 flex flex-col items-center py-4 ${menuOpen ? 'z-50' : ''}`}>
                <button
                    className="fa-solid fa-bars hover:bg-zinc-400 cursor-pointer p-2 rounded-sm"
                    onClick={handlePressMenu(menuOpen, setMenuOpen)}
                ></button>
            </div>

            {/* Side Menu */}
            <div
                className={`fixed top-0 left-0 z-50 h-full bg-neutral-900 flex transition-transform duration-300 ease-in-out ${
                menuOpen ? 'translate-x-0' : '-translate-x-full'
                }`}
            >
                <div className="border border-zinc-800 items-center">
                <div className="p-4 flex gap-8 items-center">
                    <button
                    className="fa-solid fa-bars hover:bg-zinc-400 cursor-pointer p-2 rounded-sm"
                    onClick={handlePressMenu(menuOpen, setMenuOpen)}
                    ></button>
                    <div className="flex items-center gap-2 px-4">
                    <img src={images.logoAI} alt="logo" className="h-8 w-8 rounded-full bg-blue-500" />
                    <span className="font-semibold text-lg">AIGen</span>
                    </div>
                </div>
                <ul className="gap-2 flex flex-col px-4 mt-2">
                    <li 
                        className="hover:bg-neutral-500 cursor-pointer p-2 rounded-sm"
                        onClick={() => navigate("/home")}
                    >
                        <i className="fa-solid fa-house mr-2 text-2xl"></i>
                        Home
                    </li>

                    <li 
                        className="hover:bg-neutral-500 cursor-pointer p-2 rounded-sm"
                        onClick={() => navigate("/dashboard")}
                    >
                        <i className="fa-solid fa-square-poll-horizontal mr-2 text-2xl">
                        </i>
                        Dashboard
                    </li>

                    <li 
                        className="hover:bg-neutral-500 cursor-pointer p-2 rounded-sm"
                        onClick={() => navigate("/analyst")}
                    >
                        <i className="fa-solid fa-gears mr-2 text-2xl"></i>
                        Analyst
                    </li>
                </ul>
                </div>
            </div>

        </div>
    )
}

export default LeftSideBar;