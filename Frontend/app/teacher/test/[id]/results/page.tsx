"use client"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ArrowLeft, Download, Eye, BarChart3, Users, Clock, CheckCircle, XCircle } from "lucide-react"
import Link from "next/link"
import { useParams } from "next/navigation"

export default function TestResults() {
  const params = useParams()

  // Mock data
  const test = {
    id: params.id,
    title: "Matematika - Algebra asoslari",
    subject: "Matematika",
    questions: 25,
    duration: 60,
    totalStudents: 23,
    completed: 18,
    averageScore: 78,
    averageTime: 45,
  }

  const studentResults = [
    { id: 1, name: "Aziza Karimova", score: 95, correct: 24, time: 42, status: "completed" },
    { id: 2, name: "Bobur Rahimov", score: 88, correct: 22, time: 38, status: "completed" },
    { id: 3, name: "Dilnoza Tosheva", score: 92, correct: 23, time: 45, status: "completed" },
    { id: 4, name: "Eldor Nazarov", score: 76, correct: 19, time: 52, status: "completed" },
    { id: 5, name: "Feruza Alimova", score: 84, correct: 21, time: 41, status: "completed" },
    { id: 6, name: "Gulnoza Saidova", score: 0, correct: 0, time: 0, status: "in-progress" },
    { id: 7, name: "Husan Toshev", score: 72, correct: 18, time: 55, status: "completed" },
  ]

  const questionAnalysis = [
    { id: 1, question: "2x + 5 = 15 tenglamani yeching", correct: 16, incorrect: 2, difficulty: "Oson" },
    { id: 2, question: "Kvadrat tenglamaning diskriminantini toping", correct: 12, incorrect: 6, difficulty: "O'rta" },
    { id: 3, question: "Logarifm xossalarini qo'llang", correct: 8, incorrect: 10, difficulty: "Qiyin" },
    { id: 4, question: "Trigonometrik tenglamani yeching", correct: 14, incorrect: 4, difficulty: "O'rta" },
    { id: 5, question: "Kompleks sonlar bilan amallar", correct: 6, incorrect: 12, difficulty: "Qiyin" },
  ]

  const getScoreColor = (score: number) => {
    if (score >= 90) return "text-green-600"
    if (score >= 70) return "text-blue-600"
    if (score >= 50) return "text-yellow-600"
    return "text-red-600"
  }

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case "Oson":
        return "bg-green-100 text-green-800"
      case "O'rta":
        return "bg-yellow-100 text-yellow-800"
      case "Qiyin":
        return "bg-red-100 text-red-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
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
                <h1 className="text-2xl font-bold text-gray-900">Test natijalari</h1>
                <p className="text-gray-600">{test.title}</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Button variant="outline">
                <Download className="w-4 h-4 mr-2" />
                Excel yuklab olish
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {/* Overview Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Jami o'quvchilar</p>
                  <p className="text-3xl font-bold text-gray-900">{test.totalStudents}</p>
                </div>
                <Users className="w-8 h-8 text-blue-600" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Tugallangan</p>
                  <p className="text-3xl font-bold text-green-600">{test.completed}</p>
                </div>
                <CheckCircle className="w-8 h-8 text-green-600" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">O'rtacha ball</p>
                  <p className="text-3xl font-bold text-purple-600">{test.averageScore}%</p>
                </div>
                <BarChart3 className="w-8 h-8 text-purple-600" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">O'rtacha vaqt</p>
                  <p className="text-3xl font-bold text-orange-600">{test.averageTime} daq</p>
                </div>
                <Clock className="w-8 h-8 text-orange-600" />
              </div>
            </CardContent>
          </Card>
        </div>

        <Tabs defaultValue="students" className="space-y-6">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="students">O'quvchilar natijalari</TabsTrigger>
            <TabsTrigger value="questions">Savollar tahlili</TabsTrigger>
          </TabsList>

          {/* Students Results */}
          <TabsContent value="students" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>O'quvchilar ro'yxati</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {studentResults.map((student, index) => (
                    <div key={student.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                      <div className="flex items-center space-x-4">
                        <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white font-semibold">
                          {index + 1}
                        </div>
                        <div>
                          <p className="font-medium text-gray-900">{student.name}</p>
                          <div className="flex items-center space-x-4 text-sm text-gray-600">
                            <span>
                              {student.correct}/{test.questions} to'g'ri
                            </span>
                            <span>{student.time} daqiqa</span>
                            <Badge variant={student.status === "completed" ? "default" : "secondary"}>
                              {student.status === "completed" ? "Tugallangan" : "Jarayonda"}
                            </Badge>
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center space-x-4">
                        <div className="text-right">
                          <p className={`text-2xl font-bold ${getScoreColor(student.score)}`}>{student.score}%</p>
                        </div>
                        <Button variant="outline" size="sm">
                          <Eye className="w-4 h-4 mr-1" />
                          Batafsil
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Questions Analysis */}
          <TabsContent value="questions" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Savollar bo'yicha tahlil</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {questionAnalysis.map((question) => (
                    <div key={question.id} className="border rounded-lg p-4">
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex-1">
                          <h4 className="font-medium text-gray-900 mb-2">
                            Savol {question.id}: {question.question}
                          </h4>
                          <Badge className={getDifficultyColor(question.difficulty)}>{question.difficulty}</Badge>
                        </div>
                      </div>

                      <div className="grid grid-cols-3 gap-4 text-sm">
                        <div className="flex items-center space-x-2">
                          <CheckCircle className="w-4 h-4 text-green-600" />
                          <span className="text-green-600 font-medium">{question.correct} to'g'ri</span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <XCircle className="w-4 h-4 text-red-600" />
                          <span className="text-red-600 font-medium">{question.incorrect} noto'g'ri</span>
                        </div>
                        <div className="text-gray-600">
                          {Math.round((question.correct / (question.correct + question.incorrect)) * 100)}% muvaffaqiyat
                        </div>
                      </div>

                      {/* Progress bar */}
                      <div className="mt-3">
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div
                            className="bg-green-600 h-2 rounded-full"
                            style={{
                              width: `${(question.correct / (question.correct + question.incorrect)) * 100}%`,
                            }}
                          ></div>
                        </div>
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
