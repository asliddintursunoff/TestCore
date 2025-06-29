"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Copy, QrCode, ArrowLeft, LinkIcon, Users, Clock, FileText, CheckCircle } from "lucide-react"
import Link from "next/link"
import { useParams } from "next/navigation"

export default function ShareTest() {
  const params = useParams()
  const [copied, setCopied] = useState(false)

  // Mock test data
  const test = {
    id: params.id,
    title: "Matematika - Algebra asoslari",
    subject: "Matematika",
    questions: 25,
    duration: 60,
    link: `https://testcore.uz/t/abc123`,
    qrCode: "/placeholder.svg?height=200&width=200",
  }

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(test.link)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error("Failed to copy: ", err)
    }
  }

  const shareViaWhatsApp = () => {
    const message = `Test: ${test.title}\nHavola: ${test.link}`
    window.open(`https://wa.me/?text=${encodeURIComponent(message)}`, "_blank")
  }

  const shareViaTelegram = () => {
    const message = `Test: ${test.title}\nHavola: ${test.link}`
    window.open(
      `https://t.me/share/url?url=${encodeURIComponent(test.link)}&text=${encodeURIComponent(message)}`,
      "_blank",
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Button variant="outline" size="sm" asChild>
                <Link href="/teacher">
                  <ArrowLeft className="w-4 h-4 mr-2" />
                  Orqaga
                </Link>
              </Button>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Testni ulashish</h1>
                <p className="text-gray-600">O'quvchilar bilan test havolasini ulashing</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Test Info */}
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Test ma'lumotlari</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">{test.title}</h3>
                  <Badge variant="secondary" className="mt-2">
                    {test.subject}
                  </Badge>
                </div>

                <div className="grid grid-cols-3 gap-4 text-sm">
                  <div className="flex items-center space-x-2 text-gray-600">
                    <FileText className="w-4 h-4" />
                    <span>{test.questions} savol</span>
                  </div>
                  <div className="flex items-center space-x-2 text-gray-600">
                    <Clock className="w-4 h-4" />
                    <span>{test.duration} daqiqa</span>
                  </div>
                  <div className="flex items-center space-x-2 text-gray-600">
                    <Users className="w-4 h-4" />
                    <span>Cheksiz</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Share Link */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <LinkIcon className="w-5 h-5 mr-2" />
                  Test havolasi
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center space-x-2">
                  <Input value={test.link} readOnly className="font-mono text-sm" />
                  <Button onClick={copyToClipboard} variant="outline">
                    {copied ? <CheckCircle className="w-4 h-4 text-green-600" /> : <Copy className="w-4 h-4" />}
                  </Button>
                </div>

                {copied && <p className="text-sm text-green-600">Havola nusxalandi!</p>}

                <div className="flex space-x-2">
                  <Button onClick={shareViaWhatsApp} variant="outline" className="flex-1 bg-transparent">
                    WhatsApp orqali
                  </Button>
                  <Button onClick={shareViaTelegram} variant="outline" className="flex-1 bg-transparent">
                    Telegram orqali
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* Instructions */}
            <Card>
              <CardHeader>
                <CardTitle>O'quvchilar uchun ko'rsatmalar</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2 text-sm text-gray-600">
                <p>1. Berilgan havolani bosing yoki QR kodni skanerlang</p>
                <p>2. Telegram orqali tizimga kiring</p>
                <p>3. Test boshlangunga qadar kutib turing</p>
                <p>4. Vaqt tugagunga qadar barcha savollarga javob bering</p>
                <p>5. Testni yakunlash tugmasini bosing</p>
              </CardContent>
            </Card>
          </div>

          {/* QR Code */}
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <QrCode className="w-5 h-5 mr-2" />
                  QR kod
                </CardTitle>
              </CardHeader>
              <CardContent className="text-center space-y-4">
                <div className="bg-white p-8 rounded-lg border-2 border-dashed border-gray-300 inline-block">
                  <img src={test.qrCode || "/placeholder.svg"} alt="QR Code" className="w-48 h-48 mx-auto" />
                </div>

                <p className="text-sm text-gray-600">
                  O'quvchilar ushbu QR kodni telefonlari bilan skanerlashlari mumkin
                </p>

                <Button variant="outline" className="w-full bg-transparent">
                  QR kodni yuklab olish
                </Button>
              </CardContent>
            </Card>

            {/* Live Stats */}
            <Card>
              <CardHeader>
                <CardTitle>Jonli statistika</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4 text-center">
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <p className="text-2xl font-bold text-blue-600">0</p>
                    <p className="text-sm text-gray-600">Faol o'quvchilar</p>
                  </div>
                  <div className="bg-green-50 p-4 rounded-lg">
                    <p className="text-2xl font-bold text-green-600">0</p>
                    <p className="text-sm text-gray-600">Tugallangan</p>
                  </div>
                </div>

                <div className="text-center">
                  <Button asChild>
                    <Link href={`/teacher/test/${test.id}/results`}>Natijalarni ko'rish</Link>
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
