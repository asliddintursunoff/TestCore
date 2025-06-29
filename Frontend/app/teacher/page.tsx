"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Users, FileText, Plus, Eye, Share2, QrCode, BarChart3, Clock, CheckCircle, Upload } from "lucide-react"
import Link from "next/link"

// Mock data
const teacherStats = {
  totalTests: 12,
  activeTests: 3,
  totalStudents: 45,
  completedTests: 89,
}

const recentTests = [
  {
    id: 1,
    title: "Matematika - Algebra asoslari",
    subject: "Matematika",
    questions: 25,
    duration: 60,
    students: 23,
    completed: 18,
    status: "active",
    createdAt: "2024-01-15",
    link: "https://testcore.uz/t/abc123",
  },
  {
    id: 2,
    title: "Fizika - Mexanika",
    subject: "Fizika",
    questions: 30,
    duration: 45,
    students: 20,
    completed: 20,
    status: "completed",
    createdAt: "2024-01-10",
    link: "https://testcore.uz/t/def456",
  },
  {
    id: 3,
    title: "Kimyo - Organik birikmalar",
    subject: "Kimyo",
    questions: 20,
    duration: 40,
    students: 15,
    completed: 12,
    status: "active",
    createdAt: "2024-01-12",
    link: "https://testcore.uz/t/ghi789",
  },
]

const topStudents = [
  { name: "Aziza Karimova", score: 95, tests: 8 },
  { name: "Bobur Rahimov", score: 92, tests: 7 },
  { name: "Dilnoza Tosheva", score: 89, tests: 9 },
  { name: "Eldor Nazarov", score: 87, tests: 6 },
  { name: "Feruza Alimova", score: 85, tests: 8 },
]

export default function TeacherDashboard() {
  const [selectedTest, setSelectedTest] = useState<number | null>(null)

  const getStatusColor = (status: string) => {
    switch (status) {
      case "active":
        return "bg-green-100 text-green-800"
      case "completed":
        return "bg-blue-100 text-blue-800"
      case "draft":
        return "bg-gray-100 text-gray-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  const getStatusText = (status: string) => {
    switch (status) {
      case "active":
        return "Faol"
      case "completed":
        return "Tugallangan"
      case "draft":
        return "Qoralama"
      default:
        return "Noma'lum"
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">O'qituvchi paneli</h1>
              <p className="text-gray-600">Testlar va o'quvchilarni boshqaring</p>
            </div>
            <div className="flex items-center space-x-4">
              <Button asChild>
                <Link href="/teacher/create-test">
                  <Plus className="w-4 h-4 mr-2" />
                  Yangi test
                </Link>
              </Button>
              <Button variant="outline" asChild>
                <Link href="/teacher/ai-generator">
                  <Upload className="w-4 h-4 mr-2" />
                  AI bilan yaratish
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Jami testlar</p>
                  <p className="text-3xl font-bold text-gray-900">{teacherStats.totalTests}</p>
                </div>
                <FileText className="w-8 h-8 text-blue-600" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Faol testlar</p>
                  <p className="text-3xl font-bold text-green-600">{teacherStats.activeTests}</p>
                </div>
                <CheckCircle className="w-8 h-8 text-green-600" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">O'quvchilar</p>
                  <p className="text-3xl font-bold text-purple-600">{teacherStats.totalStudents}</p>
                </div>
                <Users className="w-8 h-8 text-purple-600" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Bajarilgan</p>
                  <p className="text-3xl font-bold text-orange-600">{teacherStats.completedTests}</p>
                </div>
                <BarChart3 className="w-8 h-8 text-orange-600" />
              </div>
            </CardContent>
          </Card>
        </div>

        <Tabs defaultValue="tests" className="space-y-6">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="tests">Mening testlarim</TabsTrigger>
            <TabsTrigger value="students">O'quvchilar</TabsTrigger>
            <TabsTrigger value="results">Natijalar</TabsTrigger>
          </TabsList>

          {/* Tests Tab */}
          <TabsContent value="tests" className="space-y-6">
            <div className="grid gap-6">
              {recentTests.map((test) => (
                <Card key={test.id} className="hover:shadow-lg transition-shadow">
                  <CardContent className="p-6">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <h3 className="text-lg font-semibold text-gray-900">{test.title}</h3>
                          <Badge className={getStatusColor(test.status)}>{getStatusText(test.status)}</Badge>
                        </div>

                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4 text-sm text-gray-600">
                          <div className="flex items-center">
                            <FileText className="w-4 h-4 mr-1" />
                            {test.questions} savol
                          </div>
                          <div className="flex items-center">
                            <Clock className="w-4 h-4 mr-1" />
                            {test.duration} daqiqa
                          </div>
                          <div className="flex items-center">
                            <Users className="w-4 h-4 mr-1" />
                            {test.students} o'quvchi
                          </div>
                          <div className="flex items-center">
                            <CheckCircle className="w-4 h-4 mr-1" />
                            {test.completed}/{test.students} bajarilgan
                          </div>
                        </div>

                        <div className="flex items-center space-x-2 text-sm text-gray-500">
                          <span>Yaratilgan: {test.createdAt}</span>
                          <span>•</span>
                          <span className="font-mono text-xs bg-gray-100 px-2 py-1 rounded">{test.link}</span>
                        </div>
                      </div>

                      <div className="flex items-center space-x-2 ml-4">
                        <Button variant="outline" size="sm" asChild>
                          <Link href={`/teacher/test/${test.id}/results`}>
                            <Eye className="w-4 h-4 mr-1" />
                            Natijalar
                          </Link>
                        </Button>

                        <Button variant="outline" size="sm" asChild>
                          <Link href={`/teacher/test/${test.id}/share`}>
                            <Share2 className="w-4 h-4 mr-1" />
                            Ulashish
                          </Link>
                        </Button>

                        <Button variant="outline" size="sm" asChild>
                          <Link href={`/teacher/test/${test.id}/qr`}>
                            <QrCode className="w-4 h-4" />
                          </Link>
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          {/* Students Tab */}
          <TabsContent value="students" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Eng faol o'quvchilar</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {topStudents.map((student, index) => (
                    <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                      <div className="flex items-center space-x-4">
                        <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white font-semibold">
                          {index + 1}
                        </div>
                        <div>
                          <p className="font-medium text-gray-900">{student.name}</p>
                          <p className="text-sm text-gray-600">{student.tests} ta test bajarilgan</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="text-lg font-semibold text-green-600">{student.score}%</p>
                        <p className="text-sm text-gray-600">O'rtacha ball</p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Results Tab */}
          <TabsContent value="results" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>So'nggi natijalar</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {[
                    {
                      student: "Aziza Karimova",
                      test: "Matematika - Algebra",
                      score: 95,
                      time: "45 daq",
                      date: "2024-01-15",
                    },
                    {
                      student: "Bobur Rahimov",
                      test: "Fizika - Mexanika",
                      score: 88,
                      time: "42 daq",
                      date: "2024-01-15",
                    },
                    {
                      student: "Dilnoza Tosheva",
                      test: "Matematika - Algebra",
                      score: 92,
                      time: "38 daq",
                      date: "2024-01-14",
                    },
                    {
                      student: "Eldor Nazarov",
                      test: "Kimyo - Organik",
                      score: 76,
                      time: "35 daq",
                      date: "2024-01-14",
                    },
                  ].map((result, index) => (
                    <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex-1">
                        <p className="font-medium text-gray-900">{result.student}</p>
                        <p className="text-sm text-gray-600">{result.test}</p>
                      </div>
                      <div className="flex items-center space-x-6 text-sm">
                        <div className="text-center">
                          <p className="font-semibold text-gray-900">{result.score}%</p>
                          <p className="text-gray-600">Ball</p>
                        </div>
                        <div className="text-center">
                          <p className="font-semibold text-gray-900">{result.time}</p>
                          <p className="text-gray-600">Vaqt</p>
                        </div>
                        <div className="text-center">
                          <p className="font-semibold text-gray-900">{result.date}</p>
                          <p className="text-gray-600">Sana</p>
                        </div>
                        <Button variant="outline" size="sm">
                          <Eye className="w-4 h-4 mr-1" />
                          Ko'rish
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
