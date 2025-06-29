"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Plus, Trash2, Save, Eye, ArrowLeft, Upload, FileText, Clock, Users } from "lucide-react"
import Link from "next/link"

interface Question {
  id: number
  question: string
  options: string[]
  correctAnswer: number
  explanation?: string
}

export default function CreateTest() {
  const [testTitle, setTestTitle] = useState("")
  const [testDescription, setTestDescription] = useState("")
  const [testDuration, setTestDuration] = useState("60")
  const [testSubject, setTestSubject] = useState("")
  const [questions, setQuestions] = useState<Question[]>([
    {
      id: 1,
      question: "",
      options: ["", "", "", ""],
      correctAnswer: 0,
      explanation: "",
    },
  ])

  const addQuestion = () => {
    const newQuestion: Question = {
      id: questions.length + 1,
      question: "",
      options: ["", "", "", ""],
      correctAnswer: 0,
      explanation: "",
    }
    setQuestions([...questions, newQuestion])
  }

  const removeQuestion = (id: number) => {
    setQuestions(questions.filter((q) => q.id !== id))
  }

  const updateQuestion = (id: number, field: keyof Question, value: any) => {
    setQuestions(questions.map((q) => (q.id === id ? { ...q, [field]: value } : q)))
  }

  const updateOption = (questionId: number, optionIndex: number, value: string) => {
    setQuestions(
      questions.map((q) =>
        q.id === questionId ? { ...q, options: q.options.map((opt, idx) => (idx === optionIndex ? value : opt)) } : q,
      ),
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
                <h1 className="text-2xl font-bold text-gray-900">Yangi test yaratish</h1>
                <p className="text-gray-600">Test ma'lumotlarini to'ldiring va savollar qo'shing</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Button variant="outline">
                <Eye className="w-4 h-4 mr-2" />
                Ko'rib chiqish
              </Button>
              <Button>
                <Save className="w-4 h-4 mr-2" />
                Saqlash
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Test Information */}
            <Card>
              <CardHeader>
                <CardTitle>Test ma'lumotlari</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="title">Test nomi</Label>
                  <Input
                    id="title"
                    value={testTitle}
                    onChange={(e) => setTestTitle(e.target.value)}
                    placeholder="Masalan: Matematika - Algebra asoslari"
                  />
                </div>

                <div>
                  <Label htmlFor="description">Tavsif</Label>
                  <Textarea
                    id="description"
                    value={testDescription}
                    onChange={(e) => setTestDescription(e.target.value)}
                    placeholder="Test haqida qisqacha ma'lumot..."
                    rows={3}
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="subject">Fan</Label>
                    <Select value={testSubject} onValueChange={setTestSubject}>
                      <SelectTrigger>
                        <SelectValue placeholder="Fanni tanlang" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="matematika">Matematika</SelectItem>
                        <SelectItem value="fizika">Fizika</SelectItem>
                        <SelectItem value="kimyo">Kimyo</SelectItem>
                        <SelectItem value="biologiya">Biologiya</SelectItem>
                        <SelectItem value="tarix">Tarix</SelectItem>
                        <SelectItem value="adabiyot">Adabiyot</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <Label htmlFor="duration">Davomiyligi (daqiqa)</Label>
                    <Input
                      id="duration"
                      type="number"
                      value={testDuration}
                      onChange={(e) => setTestDuration(e.target.value)}
                      placeholder="60"
                    />
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Questions */}
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle>Savollar ({questions.length})</CardTitle>
                  <Button onClick={addQuestion}>
                    <Plus className="w-4 h-4 mr-2" />
                    Savol qo'shish
                  </Button>
                </div>
              </CardHeader>
              <CardContent className="space-y-6">
                {questions.map((question, index) => (
                  <div key={question.id} className="border rounded-lg p-6 space-y-4">
                    <div className="flex items-center justify-between">
                      <h4 className="font-medium text-gray-900">Savol {index + 1}</h4>
                      {questions.length > 1 && (
                        <Button variant="outline" size="sm" onClick={() => removeQuestion(question.id)}>
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      )}
                    </div>

                    <div>
                      <Label>Savol matni</Label>
                      <Textarea
                        value={question.question}
                        onChange={(e) => updateQuestion(question.id, "question", e.target.value)}
                        placeholder="Savolingizni kiriting..."
                        rows={2}
                      />
                    </div>

                    <div className="space-y-2">
                      <Label>Javob variantlari</Label>
                      {question.options.map((option, optionIndex) => (
                        <div key={optionIndex} className="flex items-center space-x-2">
                          <input
                            type="radio"
                            name={`correct-${question.id}`}
                            checked={question.correctAnswer === optionIndex}
                            onChange={() => updateQuestion(question.id, "correctAnswer", optionIndex)}
                            className="text-blue-600"
                          />
                          <Input
                            value={option}
                            onChange={(e) => updateOption(question.id, optionIndex, e.target.value)}
                            placeholder={`Variant ${optionIndex + 1}`}
                          />
                        </div>
                      ))}
                    </div>

                    <div>
                      <Label>Tushuntirish (ixtiyoriy)</Label>
                      <Textarea
                        value={question.explanation || ""}
                        onChange={(e) => updateQuestion(question.id, "explanation", e.target.value)}
                        placeholder="To'g'ri javob uchun tushuntirish..."
                        rows={2}
                      />
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Quick Actions */}
            <Card>
              <CardHeader>
                <CardTitle>Tez amallar</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button variant="outline" className="w-full justify-start bg-transparent" asChild>
                  <Link href="/teacher/ai-generator">
                    <Upload className="w-4 h-4 mr-2" />
                    AI bilan yaratish
                  </Link>
                </Button>
                <Button variant="outline" className="w-full justify-start bg-transparent">
                  <FileText className="w-4 h-4 mr-2" />
                  Shablondan import
                </Button>
              </CardContent>
            </Card>

            {/* Test Preview */}
            <Card>
              <CardHeader>
                <CardTitle>Test ko'rinishi</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center space-x-2 text-sm text-gray-600">
                  <FileText className="w-4 h-4" />
                  <span>{questions.length} savol</span>
                </div>
                <div className="flex items-center space-x-2 text-sm text-gray-600">
                  <Clock className="w-4 h-4" />
                  <span>{testDuration} daqiqa</span>
                </div>
                <div className="flex items-center space-x-2 text-sm text-gray-600">
                  <Users className="w-4 h-4" />
                  <span>Cheklanmagan o'quvchi</span>
                </div>

                {testSubject && <Badge variant="secondary">{testSubject}</Badge>}
              </CardContent>
            </Card>

            {/* Tips */}
            <Card>
              <CardHeader>
                <CardTitle>Maslahatlar</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2 text-sm text-gray-600">
                <p>• Savollarni aniq va tushunarli qilib yozing</p>
                <p>• Har bir savol uchun to'g'ri javobni belgilang</p>
                <p>• Tushuntirishlar qo'shish o'quvchilarga yordam beradi</p>
                <p>• Test davomiyligini savollar soniga mos qiling</p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
