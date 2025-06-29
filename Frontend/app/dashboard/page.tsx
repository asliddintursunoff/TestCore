"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { GraduationCap, Trophy, User, FileText, Medal, LogOut, Menu, X, Crown, School, University } from "lucide-react"
import Link from "next/link"

export default function Dashboard() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                <GraduationCap className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-900">TestCore.uz</span>
            </div>

            {/* Hamburger Menu */}
            <Button variant="outline" size="sm" onClick={toggleMenu}>
              {isMenuOpen ? <X className="w-4 h-4" /> : <Menu className="w-4 h-4" />}
            </Button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="bg-white border-t">
            <div className="container mx-auto px-4 py-4 space-y-2">
              <Link
                href="/profile"
                className="flex items-center space-x-2 p-2 hover:bg-gray-100 rounded-lg"
                onClick={() => setIsMenuOpen(false)}
              >
                <User className="w-4 h-4" />
                <span>Mening profilim</span>
              </Link>
              <Link
                href="/my-tests"
                className="flex items-center space-x-2 p-2 hover:bg-gray-100 rounded-lg"
                onClick={() => setIsMenuOpen(false)}
              >
                <FileText className="w-4 h-4" />
                <span>Ishlangan testlarim</span>
              </Link>
              <Link
                href="/olympiads"
                className="flex items-center space-x-2 p-2 hover:bg-gray-100 rounded-lg"
                onClick={() => setIsMenuOpen(false)}
              >
                <Medal className="w-4 h-4" />
                <span>Olimpiadalar</span>
              </Link>
              <Link
                href="/teacher"
                className="flex items-center space-x-2 p-2 hover:bg-gray-100 rounded-lg"
                onClick={() => setIsMenuOpen(false)}
              >
                <Crown className="w-4 h-4" />
                <span>O'qituvchi paneli</span>
              </Link>
              <button className="flex items-center space-x-2 p-2 hover:bg-gray-100 rounded-lg w-full text-left text-red-600">
                <LogOut className="w-4 h-4" />
                <span>Chiqish</span>
              </button>
            </div>
          </div>
        )}
      </header>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Xush kelibsiz!</h1>
          <p className="text-gray-600">Test turini tanlab, tayyorgarlikni boshlang</p>
        </div>

        {/* Test Categories */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {/* Presidential School Tests */}
          <Card className="hover:shadow-lg transition-shadow cursor-pointer border-2 border-yellow-200 hover:border-yellow-400">
            <CardContent className="p-8 text-center">
              <div className="w-16 h-16 bg-yellow-600 rounded-full flex items-center justify-center mx-auto mb-6">
                <Crown className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Prezident maktabi testlari</h3>
              <p className="text-gray-600 mb-6">
                Prezident maktablariga kirish uchun maxsus tayyorlangan testlar va mashqlar
              </p>
              <Button className="w-full bg-yellow-600 hover:bg-yellow-700" asChild>
                <Link href="/tests/presidential">Testlarni ko'rish</Link>
              </Button>
            </CardContent>
          </Card>

          {/* DTM Tests */}
          <Card className="hover:shadow-lg transition-shadow cursor-pointer border-2 border-green-200 hover:border-green-400">
            <CardContent className="p-8 text-center">
              <div className="w-16 h-16 bg-green-600 rounded-full flex items-center justify-center mx-auto mb-6">
                <School className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">DTM testlari</h3>
              <p className="text-gray-600 mb-6">Davlat test markazi formatidagi testlar va tayyorgarlik materiallari</p>
              <Button className="w-full bg-green-600 hover:bg-green-700" asChild>
                <Link href="/tests/dtm">Testlarni ko'rish</Link>
              </Button>
            </CardContent>
          </Card>

          {/* University Tests */}
          <Card className="hover:shadow-lg transition-shadow cursor-pointer border-2 border-blue-200 hover:border-blue-400">
            <CardContent className="p-8 text-center">
              <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-6">
                <University className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Universitet testlari</h3>
              <p className="text-gray-600 mb-6">Turli universitetlar va fakultetlar uchun moslashtirilgan testlar</p>
              <Button className="w-full bg-blue-600 hover:bg-blue-700" asChild>
                <Link href="/universities">Universitetlarni ko'rish</Link>
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Premium Services */}
        <Card className="bg-gradient-to-r from-purple-600 to-blue-600 text-white mb-8">
          <CardContent className="p-8">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-2xl font-bold mb-2">Premium xizmatlar</h3>
                <p className="text-purple-100 mb-4">Cheksiz testlar, AI tahlil va qo'shimcha imkoniyatlar</p>
                <Button variant="secondary" asChild>
                  <Link href="/subscription">Tariflarni ko'rish</Link>
                </Button>
              </div>
              <div className="hidden md:block">
                <Trophy className="w-24 h-24 text-purple-200" />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Quick Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Card>
            <CardContent className="p-4 text-center">
              <div className="text-2xl font-bold text-blue-600">1,250+</div>
              <div className="text-sm text-gray-600">Testlar</div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4 text-center">
              <div className="text-2xl font-bold text-green-600">15,000+</div>
              <div className="text-sm text-gray-600">O'quvchilar</div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4 text-center">
              <div className="text-2xl font-bold text-purple-600">50+</div>
              <div className="text-sm text-gray-600">Universitetlar</div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4 text-center">
              <div className="text-2xl font-bold text-orange-600">95%</div>
              <div className="text-sm text-gray-600">Muvaffaqiyat</div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
