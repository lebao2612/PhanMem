import { useState, useEffect } from "react";
import Header from "../components/Header";
import LeftSideBar from "../components/LeftSideBar";
import { FaYoutube, FaFacebook, FaTiktok, FaFilm, FaCamera, FaEye } from 'react-icons/fa';
import { X, Calendar, Tag, Play } from "lucide-react"
import images from "../assets/images";

const Dashboard = () => {

    const options = ["Tất cả", "Youtube", "Facebook", "Tiktok"]
    
    const videos = [
        {name: "test1", date: "26-12-2004", tag: "Youtube", videoURL: "https://www.w3schools.com/html/mov_bbb.mp4"},
        {name: "test2", date: "26-12-2004", tag: "Youtube", videoURL: "https://www.w3schools.com/html/mov_bbb.mp4"},
        {name: "test3 asf asjfh fasfj", date: "26-12-2004", tag: "Facebook", videoURL: "https://www.w3schools.com/html/mov_bbb.mp4"},
        {name: "test4", date: "26-12-2004", tag: "Facebook", videoURL: "https://www.w3schools.com/html/mov_bbb.mp4"},
        {name: "test5", date: "26-12-2004", tag: "Tiktok", videoURL: "https://www.w3schools.com/html/mov_bbb.mp4"},
        {name: "test6", date: "26-12-2004", tag: "Tiktok", videoURL: "https://www.w3schools.com/html/mov_bbb.mp4"},
        {name: "test7", date: "26-12-2004", tag: "", videoURL: "https://www.w3schools.com/html/mov_bbb.mp4"},
    ]

    // const [videos, setVideos] = useState([]);

    // useEffect(() => {
    //     fetch("http://localhost:5000/api/videos") // Hoặc endpoint thật của bạn
    //         .then(res => res.json())
    //         .then(data => {
    //             setVideos(data);
    //             setFilteredVideo(data); // Đặt dữ liệu ban đầu luôn là toàn bộ video
    //         })
    //         .catch(err => console.error("Lỗi khi gọi API:", err));
    // }, []);

    console.log(videos)

    
    const [selectedOption, setSelectedOption] = useState("Tất cả")
    const [filteredVideo, setFilteredVideo] = useState(videos)
    const [selectedVideo, setSelectedVideo] = useState();

    useEffect(() => {
        filterVideo();
    }, [selectedOption]);


    const filterVideo = () =>{
        if(selectedOption === "Tất cả"){
            setFilteredVideo(videos);
        }
        else{
            setFilteredVideo(videos.filter(video => video.tag === selectedOption.toLowerCase()))
        }
    }

    const closeDetailVideo = () =>{
        setSelectedVideo()
    }

    return (
        <div className="relative flex bg-black text-white min-h-screen">
            <LeftSideBar />

            {/* Main Content */}
            <div className={"flex-1 flex flex-col transition-all duration-300"}>
                <Header />
                <div className="grid grid-cols-4 gap-4 px-5 py-10">
                    <div className="border border-zinc-700 bg-zinc-900 p-4 shadow-lg rounded-lg hover:bg-zinc-800 transition-colors">
                        <div className="flex items-center gap-2 mb-1">
                            <FaFilm className="text-purple-600 text-5xl p-1 bg-amber-50 rounded-3xl"/>
                            <h3 className="font-bold text-xl">Tổng số Video</h3>
                        </div>
                        <p className="text-neutral-500">Số lượng video đã tạo</p>
                        <div className="flex items-center gap-2 mt-2">
                            <FaCamera className="text-xl"/>
                            <p className="text-2xl font-bold">{videos.length}</p>
                        </div>
                    </div>

                    <div className="border border-zinc-700 bg-zinc-900 p-4 shadow-lg rounded-lg hover:bg-zinc-800 transition-colors">
                        <div className="flex items-center gap-2 mb-1">
                            <FaYoutube className="text-red-600 text-5xl p-1 bg-amber-50 rounded-3xl" />
                            <h3 className="font-bold text-xl">Youtube</h3>
                        </div>
                        <p className="text-neutral-500">Số lượng lượt xem trên Youtube</p>
                        <div className="flex items-center gap-2 mt-2">
                            <FaEye className="text-xl"/>
                            <p className="text-2xl font-bold">6</p>
                        </div>
                    </div>

                    <div className="border border-zinc-700 bg-zinc-900 p-4 shadow-lg rounded-lg hover:bg-zinc-800 transition-colors">
                        <div className="flex items-center gap-2 mb-1">
                            <FaFacebook className="text-blue-600 text-5xl p-1 bg-amber-50 rounded-3xl" />
                            <h3 className="font-bold text-xl">Facebook</h3>
                        </div>
                        <p className="text-neutral-500">Số lượng lượt xem trên Facebook</p>
                        <div className="flex items-center gap-2 mt-2">
                            <FaEye className="text-xl"/>
                            <p className="text-2xl font-bold">1</p>
                        </div>
                    </div>

                    <div className="border border-zinc-700 bg-zinc-900 p-4 shadow-lg rounded-lg hover:bg-zinc-800 transition-colors">
                        <div className="flex items-center gap-2 mb-1">
                            <FaTiktok className="text-black text-5xl p-1 bg-amber-50 rounded-3xl" />
                            <h3 className="font-bold text-xl">Tiktok</h3>
                        </div>
                        <p className="text-neutral-500">Số lượng lượt xem trên Tiktok</p>
                        <div className="flex items-center gap-2 mt-2">
                            <FaEye className="text-xl"/>
                            <p className="text-2xl font-bold">2</p>
                        </div>
                    </div>
                </div>

                <div className="px-5 py-3">
                    <ul className="inline-flex gap-3 px-4 py-1 bg-zinc-900 rounded text-white">
                        {options.map((option) => (
                            <li
                                key={option}
                                className={`cursor-pointer px-1 rounded-sm ${selectedOption === option ? "bg-zinc-500": ""}`}
                                onClick={() => setSelectedOption(option)}
                            >
                                {option}
                            </li>
                        ))}
                    </ul>
                </div>

                <div className="grid grid-cols-4 gap-4 px-5 py-10 ">
                    {filteredVideo.map((video, index) => (
                        <div
                            key={index}
                            className="bg-zinc-800 p-4 rounded-lg shadow transform transition-transform duration-200 hover:scale-105 hover:bg-zinc-700 cursor-pointer flex flex-col h-full"
                            onClick={() => {
                                setSelectedVideo(video)
                                console.log(video)
                            }}
                        >
                            <img src={images.thumbV || "/placeholder.svg"} className="w-full object-cover rounded mb-3" />
                            <div className="flex flex-col flex-grow">
                                <h3 className="text-lg font-bold mb-2 line-clamp-2 min-h-[3.5rem]">{video.name}</h3>
                                <div className="mt-auto space-y-1">
                                    <p className="text-sm text-neutral-400">Ngày: {video.createAt}</p>
                                    <p className="text-sm text-neutral-400">Tag: {video.tag}</p>
                                    <a
                                        href="https://www.youtube.com/watch?v=BcLDmO-cOaM"
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        onClick={(e) => e.stopPropagation()}
                                        className="text-blue-400 underline text-sm inline-block mt-2"
                                    >
                                        <i className="fa-solid fa-link mr-1"></i>
                                        Xem trên {video.tag}
                                    </a>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {selectedVideo && (
            <>
            {/* Backdrop */}
            <div
                className="fixed inset-0 bg-black/60 backdrop-blur-md z-40 animate-in fade-in duration-300"
                onClick={closeDetailVideo}
            />

            {/* Modal */}
            <div className="fixed inset-0 z-50 flex items-center justify-center p-4 animate-in zoom-in-95 fade-in duration-300">
                <div className="relative bg-gradient-to-br from-zinc-900 to-zinc-800 rounded-2xl shadow-2xl border border-zinc-700/50 max-w-4xl w-full max-h-[90vh] overflow-hidden">
                {/* Close Button */}
                    <button
                        variant="ghost"
                        size="icon"
                        className="absolute right-4 top-4 z-10 bg-black/20 hover:bg-black/40 text-white border-0 rounded-full backdrop-blur-sm transition-all duration-200 cursor-pointer"
                        onClick={closeDetailVideo}
                    >
                        <X className="w-5 h-5" />
                    </button>

                    {/* Content */}
                    <div className="flex flex-col lg:flex-row">
                        {/* Video Section */}
                        <div className="flex-1 p-6 pb-4 lg:pb-6">
                            <div className="relative rounded-xl overflow-hidden shadow-lg">
                                <video
                                    width="100%"
                                    height="400"
                                    controls
                                    preload="metadata"
                                    className="w-full aspect-video rounded-lg"
                                    poster="/placeholder.svg?height=400&width=600"
                                >
                                    <source src={selectedVideo.videoURL || selectedVideo.videoID} type="video/mp4" />
                                    <source src={selectedVideo.videoURL || selectedVideo.videoID} type="video/webm" />
                                    <source src={selectedVideo.videoURL || selectedVideo.videoID} type="video/ogg" />
                                    Trình duyệt của bạn không hỗ trợ thẻ video.
                                </video>
                            </div>
                        </div>

                        {/* Info Section */}
                        <div className="lg:w-80 p-6 pt-4 lg:pt-6 border-t lg:border-t-0 lg:border-l border-zinc-700/50">
                            <div className="space-y-6">
                                {/* Title */}
                                <div>
                                    <h3 className="text-xl font-bold text-white leading-tight mb-2">{selectedVideo.name}</h3>
                                    <div className="w-12 h-1 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full" />
                                </div>

                                {/* Metadata */}
                                <div className="space-y-4">
                                    <div className="flex items-center gap-3 text-zinc-300">
                                        <div className="flex items-center justify-center w-8 h-8 bg-zinc-700/50 rounded-lg">
                                            <Calendar className="w-4 h-4" />
                                        </div>
                                        <div>
                                            <p className="text-xs text-zinc-400 uppercase tracking-wide font-medium">Ngày phát hành</p>
                                            <p className="text-sm font-medium">{selectedVideo.createAt}</p>
                                        </div>
                                    </div>

                                    <div className="flex items-center gap-3 text-zinc-300">
                                        <div className="flex items-center justify-center w-8 h-8 bg-zinc-700/50 rounded-lg">
                                            <Tag className="w-4 h-4" />
                                        </div>
                                        <div>
                                            <p className="text-xs text-zinc-400 uppercase tracking-wide font-medium">Xuất bản</p>
                                            <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-purple-500/20 text-purple-300 border border-purple-500/30">
                                                {selectedVideo.tag !== "" ? selectedVideo.tag.toUpperCase() :"None"}
                                            </span>
                                        </div>
                                    </div>
                                </div>

                                {/* Additional Info */}
                                <div className="pt-4 border-t border-zinc-700/50">
                                    <p className="text-sm text-zinc-400 leading-relaxed">
                                        Khám phá thế giới tự nhiên qua những thước phim tuyệt đẹp với chất lượng 4K sắc nét.
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            </>
        )}

        </div>
    )
}

export default Dashboard;