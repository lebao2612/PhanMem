"use client"

import Header from "../components/Header"
import LeftSideBar from "../components/LeftSideBar"
import { useState } from "react"
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from "chart.js"
import { Line, Bar } from "react-chartjs-2"

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend, Filler)

const AnalystPage = () => {
  const [selectedPeriod, setSelectedPeriod] = useState("7days")

  // Mock data for YouTube video analytics
  const viewsData = [
    { date: "2024-01-01", views: 69, likes: 4, comments: 2 },
    { date: "2024-01-02", views: 100, likes: 6, comments: 4 },
    { date: "2024-01-03", views: 137, likes: 8, comments: 5 },
    { date: "2024-01-04", views: 203, likes: 11, comments: 7 },
    { date: "2024-01-05", views: 248, likes: 14, comments: 9 },
    { date: "2024-01-06", views: 299, likes: 17, comments: 10 },
    { date: "2024-01-07", views: 324, likes: 23, comments: 13 },
    { date: "2024-01-08", views: 372, likes: 29, comments: 17 },
    { date: "2024-01-09", views: 487, likes: 35, comments: 19 },
    { date: "2024-01-10", views: 512, likes: 44, comments: 25 },
  ]

  const videoComparisonData = [
    { video: "Video 1", views: 413, likes: 12, comments: 5 },
    { video: "Video 2", views: 28, likes: 5, comments: 2 },
    { video: "Video 3", views: 15, likes: 3, comments: 1 },
    { video: "Video 4", views: 1, likes: 0, comments: 0 },
    { video: "Video 5", views: 3, likes: 1, comments: 0 },
    { video: "Video 6", views: 249, likes: 10, comments: 7 },
    { video: "Video 7", views: 136, likes: 7, comments: 5 },
    { video: "Video 8", views: 79, likes: 6, comments: 5 },
  ]

  const totalViews = videoComparisonData.reduce((sum, video) => sum + video.views, 0)
  const totalLikes = videoComparisonData.reduce((sum, video) => sum + video.likes, 0)
  const totalComments = videoComparisonData.reduce((sum, video) => sum + video.comments, 0)

  const engagementData = [
    { metric: "Views", value: totalViews, change: "+15.2%", icon: "👁️", color: "blue" },
    { metric: "Likes", value: totalLikes, change: "+8.7%", icon: "❤️", color: "red" },
    { metric: "Comments", value: totalComments, change: "+12.3%", icon: "💬", color: "green" },
    { metric: "Shares", value: 0, change: "+0.0%", icon: "📤", color: "purple" }, // Hoặc bạn có thể bỏ mục này nếu chưa có data
  ]

  // Chart data configurations
  const viewsChartData = {
    labels: viewsData.map((item) =>
      new Date(item.date).toLocaleDateString("en-US", { month: "short", day: "numeric" }),
    ),
    datasets: [
      {
        label: "Views",
        data: viewsData.map((item) => item.views),
        borderColor: "rgb(59, 130, 246)",
        backgroundColor: "rgba(59, 130, 246, 0.1)",
        fill: true,
        tension: 0.4,
        pointBackgroundColor: "rgb(59, 130, 246)",
        pointBorderColor: "rgb(59, 130, 246)",
        pointRadius: 4,
      },
    ],
  }

  const engagementChartData = {
    labels: viewsData.map((item) =>
      new Date(item.date).toLocaleDateString("en-US", { month: "short", day: "numeric" }),
    ),
    datasets: [
      {
        label: "Likes",
        data: viewsData.map((item) => item.likes),
        borderColor: "rgb(239, 68, 68)",
        backgroundColor: "rgba(239, 68, 68, 0.1)",
        tension: 0.4,
        pointBackgroundColor: "rgb(239, 68, 68)",
        pointRadius: 3,
      },
      {
        label: "Comments",
        data: viewsData.map((item) => item.comments),
        borderColor: "rgb(34, 197, 94)",
        backgroundColor: "rgba(34, 197, 94, 0.1)",
        tension: 0.4,
        pointBackgroundColor: "rgb(34, 197, 94)",
        pointRadius: 3,
      },
    ],
  }

  const videoComparisonChartData = {
    labels: videoComparisonData.map((item) => item.video),
    datasets: [
      {
        label: "Views",
        data: videoComparisonData.map((item) => item.views),
        backgroundColor: [
          "rgba(59, 130, 246, 0.8)",
          "rgba(239, 68, 68, 0.8)",
          "rgba(34, 197, 94, 0.8)",
          "rgba(168, 85, 247, 0.8)",
          "rgba(245, 158, 11, 0.8)",
        ],
        borderColor: [
          "rgb(59, 130, 246)",
          "rgb(239, 68, 68)",
          "rgb(34, 197, 94)",
          "rgb(168, 85, 247)",
          "rgb(245, 158, 11)",
        ],
        borderWidth: 2,
        borderRadius: 4,
      },
    ],
  }

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: {
          color: "white",
          font: {
            size: 12,
          },
        },
      },
      tooltip: {
        backgroundColor: "rgba(17, 24, 39, 0.9)",
        titleColor: "white",
        bodyColor: "white",
        borderColor: "rgba(75, 85, 99, 0.5)",
        borderWidth: 1,
      },
    },
    scales: {
      x: {
        ticks: {
          color: "rgb(156, 163, 175)",
          font: {
            size: 11,
          },
        },
        grid: {
          color: "rgba(75, 85, 99, 0.3)",
        },
      },
      y: {
        ticks: {
          color: "rgb(156, 163, 175)",
          font: {
            size: 11,
          },
        },
        grid: {
          color: "rgba(75, 85, 99, 0.3)",
        },
      },
    },
  }

  return (
    <div className="relative flex min-h-screen bg-black text-white ">
      <LeftSideBar />
      <div className="flex-1 flex flex-col transition-all duration-300">

        {/* Analytics Header */}
        <div className="bg-black border-b border-gray-800 p-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-white">Analytics Dashboard</h1>
              <p className="text-gray-400 text-sm mt-1">Track your YouTube video performance</p>
            </div>
            {/*<div className="flex items-center gap-4">
              <select
                className="px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                value={selectedPeriod}
                onChange={(e) => setSelectedPeriod(e.target.value)}
              >
                <option value="7days">Last 7 Days</option>
                <option value="30days">Last 30 Days</option>
                <option value="90days">Last 90 Days</option>
                <option value="1year">Last Year</option>
              </select>
              
            </div>*/}
          </div>
        </div>

        {/* Main Content - Fixed height to prevent overflow */}
        <main className="flex-1 overflow-auto p-6 space-y-6 bg-black">
          {/* Key Metrics Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {engagementData.map((item, index) => (
              <div
                key={index}
                className="bg-gray-900 border border-gray-800 rounded-xl p-6 hover:border-gray-700 transition-colors"
              >
                <div className="flex items-center justify-between mb-4">
                  <div
                    className={`w-12 h-12 rounded-lg flex items-center justify-center ${
                      item.color === "blue"
                        ? "bg-blue-500/20"
                        : item.color === "red"
                          ? "bg-red-500/20"
                          : item.color === "green"
                            ? "bg-green-500/20"
                            : "bg-purple-500/20"
                    }`}
                  >
                    <span className="text-xl">{item.icon}</span>
                  </div>
                  <div className="text-right">
                    <p className="text-xs text-gray-400 uppercase tracking-wide font-medium">{item.metric}</p>
                  </div>
                </div>
                <div className="text-3xl font-bold text-white mb-2">{item.value.toLocaleString()}</div>
                <div className="flex items-center gap-2">
                  <span className="text-green-400 text-sm font-medium">{item.change}</span>
                  <span className="text-gray-500 text-xs">vs last period</span>
                </div>
              </div>
            ))}
          </div>

          {/* Views Trend Chart */}
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-xl font-bold text-white mb-2">Views Trend</h2>
                <p className="text-gray-400 text-sm">Daily views performance over time</p>
              </div>
              <div className="flex items-center gap-2 text-sm text-gray-400">
                <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                <span>Total Views</span>
              </div>
            </div>
            <div className="h-80">
              <Line data={viewsChartData} options={chartOptions} />
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Engagement Metrics */}
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h2 className="text-xl font-bold text-white mb-2">Engagement Metrics</h2>
                  <p className="text-gray-400 text-sm">Likes and comments interaction</p>
                </div>
                <div className="flex items-center gap-4 text-sm text-gray-400">
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                    <span>Likes</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                    <span>Comments</span>
                  </div>
                </div>
              </div>
              <div className="h-64">
                <Line data={engagementChartData} options={chartOptions} />
              </div>
            </div>

            {/* Video Comparison */}
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
              <div className="mb-6">
                <h2 className="text-xl font-bold text-white mb-2">Video Performance</h2>
                <p className="text-gray-400 text-sm">Views comparison across recent videos</p>
              </div>
              <div className="h-64">
                <Bar data={videoComparisonChartData} options={chartOptions} />
              </div>
            </div>
          </div>

          {/* Additional Stats Cards */}
          {/* <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
              <div className="flex items-center gap-4 mb-4">
                <div className="w-12 h-12 bg-blue-500/20 rounded-xl flex items-center justify-center">
                  <span className="text-blue-400 text-xl">⏱️</span>
                </div>
                <div>
                  <h3 className="text-white font-semibold">Avg. Watch Time</h3>
                  <p className="text-gray-400 text-sm">Per video session</p>
                </div>
              </div>
              <div className="text-3xl font-bold text-white mb-2">4:32</div>
              <div className="flex items-center gap-2">
                <span className="text-green-400 text-sm font-medium">+12%</span>
                <span className="text-gray-500 text-xs">vs last week</span>
              </div>
            </div>

            <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
              <div className="flex items-center gap-4 mb-4">
                <div className="w-12 h-12 bg-purple-500/20 rounded-xl flex items-center justify-center">
                  <span className="text-purple-400 text-xl">👥</span>
                </div>
                <div>
                  <h3 className="text-white font-semibold">New Subscribers</h3>
                  <p className="text-gray-400 text-sm">This week</p>
                </div>
              </div>
              <div className="text-3xl font-bold text-white mb-2">+234</div>
              <div className="flex items-center gap-2">
                <span className="text-green-400 text-sm font-medium">+18%</span>
                <span className="text-gray-500 text-xs">vs last week</span>
              </div>
            </div>

            <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
              <div className="flex items-center gap-4 mb-4">
                <div className="w-12 h-12 bg-green-500/20 rounded-xl flex items-center justify-center">
                  <span className="text-green-400 text-xl">💰</span>
                </div>
                <div>
                  <h3 className="text-white font-semibold">Est. Revenue</h3>
                  <p className="text-gray-400 text-sm">This month</p>
                </div>
              </div>
              <div className="text-3xl font-bold text-white mb-2">$1,247</div>
              <div className="flex items-center gap-2">
                <span className="text-green-400 text-sm font-medium">+25%</span>
                <span className="text-gray-500 text-xs">vs last month</span>
              </div>
            </div>
          </div> */}

          {/* Top Performing Videos */}
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
            <div className="mb-6">
              <h2 className="text-xl font-bold text-white mb-2">Top Performing Videos</h2>
              <p className="text-gray-400 text-sm">Your best content this month</p>
            </div>
            <div className="space-y-4">
              {[...videoComparisonData]
                .sort((a, b) => b.views - a.views)
                .slice(0, 3)
                .map((video, index) => (
                <div
                  key={index}
                  className="flex items-center gap-4 p-4 bg-gray-800/50 rounded-lg hover:bg-gray-800 transition-colors"
                >
                  <div className="w-16 h-12 bg-gray-700 rounded-lg flex items-center justify-center">
                    <span className="text-gray-400 text-xs">#{index + 1}</span>
                  </div>
                  <div className="flex-1">
                    <h3 className="text-white font-medium mb-1">{video.video}</h3>
                    <div className="flex items-center gap-4 text-sm text-gray-400">
                      <span>👁️ {video.views.toLocaleString()}</span>
                      <span>❤️ {video.likes}</span>
                      <span>💬 {video.comments}</span>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-green-400 font-semibold text-sm">
                      {(((video.likes + video.comments) / video.views) * 100).toFixed(1)}%
                    </div>
                    <div className="text-gray-500 text-xs">engagement</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}

export default AnalystPage
