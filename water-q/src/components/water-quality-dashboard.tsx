"use client"

import { useEffect, useState } from "react"
import { Card, CardHeader } from "@/components/ui/card"
import { CupSodaIcon, ThumbsDown, ThumbsUp, XCircle } from "lucide-react"
import { Dialog, DialogTrigger, DialogContent, DialogTitle, DialogDescription } from '@/components/ui/dialog'

// Define your water quality status function
const getWaterQualityStatus = (ppm: number) => {
  if (ppm >= 1200) {
    return {
      status: "ไม่สามารถยอมรับได้สำหรับน้ำดื่ม",  // "Unacceptable for drinking water"
      description: "ค่า PPM สูงเกินไป, น้ำไม่สามารถใช้สำหรับดื่มได้",  // "PPM value is too high, water is not safe to drink"
      color: "#D22B2B",
      icon: XCircle
    };
  }
  if (ppm >= 300) {
    return {
      status: "เเย่",  // "Bad"
      description: "คุณภาพน้ำไม่ดี, น้ำไม่แนะนำให้ดื่ม",  // "Water quality is poor, not recommended for drinking"
      color: "#D22B2B",
      icon: ThumbsDown
    };
  }
  if (ppm >= 250) {
    return {
      status: "ปานกลาง",  // "Moderate"
      description: "น้ำมีคุณภาพปานกลาง, ควรหลีกเลี่ยงการดื่มในระยะยาว",  // "Water quality is moderate, avoid long-term consumption"
      color: "#ecca00",
      icon: ThumbsDown
    };
  }
  if (ppm >= 150) {
    return {
      status: "ดี",  // "Good"
      description: "คุณภาพน้ำดี, สามารถดื่มได้ในระยะสั้น",  // "Good water quality, safe for short-term consumption"
      color: "#79c97a",
      icon: ThumbsUp
    };
  }
  return {
    status: "เหมาะสำหรับดื่ม",  // "Safe for drinking"
    description: "น้ำมีคุณภาพดีและสามารถดื่มได้อย่างปลอดภัย",  // "Water is of good quality and safe for drinking"
    color: "#79c97a",
    icon: CupSodaIcon
  };
};

export default function WaterQualityDashboard() {
  const [currentData, setCurrentData] = useState<{ tds: number, date: string } | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch("http://localhost:5000/api/latest")
      .then(res => res.json())
      .then((data: { tds: number, date: string }) => {
        setCurrentData(data)
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="text-center p-4">
        <p>Loading...</p>
      </div>
    )
  }

  if (!currentData) {
    return (
      <div className="text-center p-4">
        <p>Data not available</p>
      </div>
    )
  }

  const MAX_TDS = 1200
  const percentage = Math.round((currentData.tds / MAX_TDS) * 100);
  const dasharray = 2 * Math.PI * 109; // Circumference of the circle (radius = 109)
  const dashoffset = dasharray - (dasharray * (percentage / 100));
  const { status, color, description } = getWaterQualityStatus(currentData.tds)

  return (
    <div>
      {/* Water Quality Dashboard */}
      <div className="gap-1 justify-center items-center text-center">
        <Card>
          <CardHeader>
            <div className="flex flex-col justify-center items-center text-center">
              <div className="logo" style={{ transition: "all 1s linear" }}>
                <svg
                  width="238"
                  height="238"
                  viewBox="-29.75 -29.75 297.5 297.5"
                  version="1.1"
                  xmlns="http://www.w3.org/2000/svg"
                  style={{ transform: "rotate(-90deg)" }}
                >
                  <circle r="109" cx="119" cy="119" fill="transparent" stroke="#e0e0e0" strokeWidth="33"></circle>
                  <circle
                    r="109"
                    cx="119"
                    cy="119"
                    stroke={color}
                    strokeWidth="33"
                    strokeLinecap="round"
                    strokeDashoffset={dashoffset}
                    fill="transparent"
                    strokeDasharray={dasharray}
                  ></circle>
                  <text
                    x={119}
                    y="133px"
                    fill="#1f2937"
                    fontSize="47px"
                    fontWeight="bold"
                    textAnchor="middle"
                    style={{ transform: "rotate(90deg) translate(0px, -234px)" }}
                  >
                    {currentData.tds}
                  </text>
                </svg>
              </div>
              <div className="text">
                <h1 className="flex text-center">
                  <p className="text-gray-800">คุณภาพน้ำ</p>
                  <div className="w-2"></div>
                  <p className="text-gray-800" style={{ color: color }}>{status}</p>
                  <div className="w-2"></div>
                  <p className="text-gray-800">{description}</p>
                </h1>
              </div>
            </div>
          </CardHeader>
        </Card>
      </div>

      <div className="h-4"></div>
      <div className="w-full text-center">
        <Card>
          <h1 className="text-3xl font-bold text-center p-4">วิเคราะห์</h1>
        </Card>
      </div>
      <div className="h-4"></div>
      <div className="grid gap-3 md:grid-cols-2">
        <Card>
          <Dialog>
            <div className="h-2"></div>
            <p className="text-gray-800 w-full text-center">อัพเดตเมื่อ {currentData.date}</p>
            <DialogTrigger asChild>
              <img
                src="http://localhost:5000/img1"
                className="mx-auto p-2 cursor-pointer"  // Centers the image horizontally and adds cursor pointer
                alt="Water Quality Graph 1"
              />
            </DialogTrigger>
            <DialogContent className="w-[1000px] h-[80vh]">
              <DialogTitle>กราฟ TDS จริงและค่าเฉลี่ยเคลื่อนที่</DialogTitle>
              <DialogDescription>
                <img src="http://localhost:5000/img1" alt="Water Quality Graph 1" className="max-w-full h-auto" />
              </DialogDescription>
            </DialogContent>
          </Dialog>
        </Card>
        <Card>
          <Dialog>
            <div className="h-2"></div>
            <p className="text-gray-800 w-full text-center">อัพเดตเมื่อ {currentData.date}</p>
            <DialogTrigger asChild>
              <img
                src="http://localhost:5000/img2"
                className="mx-auto p-2 cursor-pointer"  // Centers the image horizontally and adds cursor pointer
                alt="Water Quality Graph 2"
              />
            </DialogTrigger>
            <DialogContent className="w-[1000px] h-[80vh]">
              <DialogTitle>กราฟ TDS Moving Average และการคาดการณ์</DialogTitle>
              <DialogDescription>
                <img src="http://localhost:5000/img2" alt="Water Quality Graph 2" className="max-w-full h-auto" />
              </DialogDescription>
            </DialogContent>
          </Dialog>
        </Card>
      </div>
    </div >
  )
}
