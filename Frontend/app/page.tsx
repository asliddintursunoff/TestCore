import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Clock, Settings, User, GraduationCap, Trophy, BookOpen } from "lucide-react"
import Link from "next/link"

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-white">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
              <GraduationCap className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold text-gray-900">TestCore.uz</span>
          </div>

          <nav className="hidden md:flex items-center space-x-8">
            <Link href="#courses" className="text-gray-600 hover:text-blue-600 transition-colors">
              Kurslar
            </Link>
            <Link href="#internships" className="text-gray-600 hover:text-blue-600 transition-colors">
              Amaliyot
            </Link>
            <Link href="#faq" className="text-gray-600 hover:text-blue-600 transition-colors">
              FAQ
            </Link>
            <Link href="#about" className="text-gray-600 hover:text-blue-600 transition-colors">
              Biz haqimizda
            </Link>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            Universitetga tayyorgarlik
            <span className="block text-blue-600">yangi darajada</span>
          </h1>

          <p className="text-xl text-gray-600 mb-12 max-w-3xl mx-auto">
            Abituriyentlar, Prezident maktablariga tayyorlanuvchilar va universitetga kiruvchilar uchun professional
            onlayn mock imtihonlar platformasi. Sun'iy intellekt yordamida tahlil va natijalar.
          </p>

          <div className="flex justify-center">
            <Button size="lg" className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 text-lg" asChild>
              <Link href="/dashboard">Kirish</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 px-4 bg-gray-50">
        <div className="container mx-auto">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Bizning test tizimimizning afzalliklari
          </h2>

          <div className="grid md:grid-cols-3 gap-8">
            <Card className="bg-white border-0 shadow-lg hover:shadow-xl transition-shadow">
              <CardContent className="p-8">
                <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-6">
                  <Clock className="w-6 h-6 text-blue-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">
                  Universitet imtihoniga tayyorgarlik uchun vaqtni tejaydi
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  Bizning platformamiz universitet talabalariga imtihonga tayyorgarlik jarayonini soddalashtiradi,
                  ularning mavzusi va qiyinchilik darajasiga moslashtirilgan savollarni avtomatik ravishda yaratadi. Bu
                  talabalarga asosiy tushunchalarni tushunishga va tuzilgan tarzda mashq qilishga imkon beradi.
                </p>
              </CardContent>
            </Card>

            <Card className="bg-white border-0 shadow-lg hover:shadow-xl transition-shadow">
              <CardContent className="p-8">
                <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mb-6">
                  <Settings className="w-6 h-6 text-purple-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">Haqiqiy test muhitini ta'minlaydi</h3>
                <p className="text-gray-600 leading-relaxed">
                  Tizim vaqtli sessiyalar, tasodifiy savollar va foydalanuvchi uchun qulay interfeys bilan haqiqiy
                  imtihon tajribasini taqlid qiladi. Bu talabalarga ishonchni oshirish, vaqtni yaxshiroq boshqarish va
                  haqiqiy imtihon oldidan tashvishni kamaytirish imkonini beradi.
                </p>
              </CardContent>
            </Card>

            <Card className="bg-white border-0 shadow-lg hover:shadow-xl transition-shadow">
              <CardContent className="p-8">
                <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mb-6">
                  <User className="w-6 h-6 text-green-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">
                  O'qituvchilarga dars berishga e'tibor qaratishga yordam beradi
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  Bizning platformamiz o'qituvchilar uchun test yaratish, baholash yoki talabalar ishini tekshirish
                  uchun sarflanadigan vaqtni sezilarli darajada kamaytiradi. AI yaratilgan savollar orqali o'qituvchilar
                  talabalar bilan sifatli ta'lim berish va muloqot qilishga ko'proq e'tibor qaratishlari mumkin.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Test Categories */}
      <section className="py-16 px-4">
        <div className="container mx-auto">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">Test turlari</h2>

          <div className="grid md:grid-cols-3 gap-8">
            <Card className="border-2 border-blue-200 hover:border-blue-400 transition-colors cursor-pointer">
              <CardContent className="p-8 text-center">
                <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-6">
                  <Trophy className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">Prezident maktabi testlari</h3>
                <p className="text-gray-600">Prezident maktablariga kirish uchun maxsus tayyorlangan testlar</p>
              </CardContent>
            </Card>

            <Card className="border-2 border-green-200 hover:border-green-400 transition-colors cursor-pointer">
              <CardContent className="p-8 text-center">
                <div className="w-16 h-16 bg-green-600 rounded-full flex items-center justify-center mx-auto mb-6">
                  <BookOpen className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">DTM testlari</h3>
                <p className="text-gray-600">Davlat test markazi formatidagi testlar va tayyorgarlik materiallari</p>
              </CardContent>
            </Card>

            <Card className="border-2 border-purple-200 hover:border-purple-400 transition-colors cursor-pointer">
              <CardContent className="p-8 text-center">
                <div className="w-16 h-16 bg-purple-600 rounded-full flex items-center justify-center mx-auto mb-6">
                  <GraduationCap className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">Universitet testlari</h3>
                <p className="text-gray-600">Turli universitetlar va fakultetlar uchun moslashtirilgan testlar</p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Subscription Plans */}
      <section className="py-16 px-4 bg-gray-50">
        <div className="container mx-auto">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">Tariflar</h2>

          <div className="grid md:grid-cols-4 gap-6 max-w-6xl mx-auto">
            <Card className="border-2 border-gray-200">
              <CardContent className="p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Abituriyent</h3>
                <p className="text-2xl font-bold text-green-600 mb-4">Tekin</p>
                <ul className="space-y-2 text-sm text-gray-600 mb-6">
                  <li>• Oyiga 10 ta test</li>
                  <li>• 2 marta PDF savollar</li>
                  <li>• Asosiy tahlil</li>
                </ul>
                <Button className="w-full bg-transparent" variant="outline">
                  Tanlash
                </Button>
              </CardContent>
            </Card>

            <Card className="border-2 border-blue-200">
              <CardContent className="p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Talaba</h3>
                <p className="text-2xl font-bold text-blue-600 mb-4">30,000 so'm</p>
                <ul className="space-y-2 text-sm text-gray-600 mb-6">
                  <li>• Cheksiz testlar</li>
                  <li>• 10 marta PDF savollar</li>
                  <li>• Kengaytirilgan tahlil</li>
                </ul>
                <Button className="w-full">Tanlash</Button>
              </CardContent>
            </Card>

            <Card className="border-2 border-purple-200">
              <CardContent className="p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Ustoz</h3>
                <p className="text-2xl font-bold text-purple-600 mb-4">49,999 so'm</p>
                <ul className="space-y-2 text-sm text-gray-600 mb-6">
                  <li>• Cheksiz testlar</li>
                  <li>• 25 marta PDF savollar</li>
                  <li>• O'qituvchi paneli</li>
                </ul>
                <Button className="w-full bg-transparent" variant="outline">
                  Tanlash
                </Button>
              </CardContent>
            </Card>

            <Card className="border-2 border-yellow-200">
              <CardContent className="p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Ustoz Plus</h3>
                <p className="text-2xl font-bold text-yellow-600 mb-4">99,999 so'm</p>
                <ul className="space-y-2 text-sm text-gray-600 mb-6">
                  <li>• Cheksiz testlar</li>
                  <li>• Cheksiz PDF savollar</li>
                  <li>• Premium panel</li>
                </ul>
                <Button className="w-full bg-transparent" variant="outline">
                  Tanlash
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Feedback Section */}
      <section className="py-16 px-4">
        <div className="container mx-auto max-w-2xl">
          <Card className="bg-white shadow-lg">
            <CardContent className="p-8">
              <h3 className="text-2xl font-semibold text-gray-900 mb-2">Fikr-mulohaza</h3>
              <p className="text-gray-600 mb-6">Sizning fikr-mulohazangizni kutmoqdamiz.</p>

              <div className="space-y-4">
                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                    Email
                  </label>
                  <Input id="email" type="email" placeholder="email@example.com" className="w-full" />
                </div>
                <div>
                  <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-2">
                    Xabar
                  </label>
                  <textarea
                    id="message"
                    rows={4}
                    placeholder="Sizning fikr-mulohazangiz..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <Button className="w-full bg-blue-600 hover:bg-blue-700">Yuborish</Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12 px-4">
        <div className="container mx-auto">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                  <GraduationCap className="w-5 h-5 text-white" />
                </div>
                <span className="text-xl font-bold">TestCore.uz</span>
              </div>
              <p className="text-gray-400">Professional onlayn mock imtihonlar platformasi</p>
            </div>

            <div>
              <h4 className="font-semibold mb-4">Xizmatlar</h4>
              <ul className="space-y-2 text-gray-400">
                <li>
                  <Link href="#" className="hover:text-white transition-colors">
                    Mock testlar
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white transition-colors">
                    AI tahlil
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white transition-colors">
                    Olimpiadalar
                  </Link>
                </li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold mb-4">Yordam</h4>
              <ul className="space-y-2 text-gray-400">
                <li>
                  <Link href="#" className="hover:text-white transition-colors">
                    FAQ
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white transition-colors">
                    Qo'llab-quvvatlash
                  </Link>
                </li>
                <li>
                  <Link href="#" className="hover:text-white transition-colors">
                    Bog'lanish
                  </Link>
                </li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold mb-4">Bog'lanish</h4>
              <ul className="space-y-2 text-gray-400">
                <li>info@testcore.uz</li>
                <li>+998 90 123 45 67</li>
                <li>Toshkent, O'zbekiston</li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 TestCore.uz. Barcha huquqlar himoyalangan.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
