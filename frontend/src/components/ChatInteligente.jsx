import React, { useState } from 'react'

const ChatInteligente = () => {
  const [isOpen, setIsOpen] = useState(false)

  const toggleChat = () => setIsOpen(!isOpen)

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {/* Chat desplegable */}
      {isOpen && (
        <div className="mb-4 bg-white rounded-lg shadow-xl max-w-sm w-80 border border-gray-200 animate-slide-up">
          {/* Header del chat */}
          <div className="bg-blue-600 text-white px-4 py-3 rounded-t-lg flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <div>
                <h3 className="text-sm font-semibold">Chat Inteligente</h3>
                <p className="text-xs opacity-90">Asistente virtual</p>
              </div>
            </div>
            <button
              onClick={toggleChat}
              className="text-white hover:bg-white hover:bg-opacity-20 p-1 rounded-full transition-colors"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </button>
          </div>

          {/* Contenido del chat */}
          <div className="h-80 overflow-y-auto p-4 bg-gray-50">
            <div className="space-y-3">
              {/* Mensaje del bot */}
              <div className="flex items-start gap-2">
                <div className="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <svg className="w-3 h-3 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
                <div className="bg-white rounded-lg p-3 shadow-sm max-w-xs">
                  <p className="text-xs text-gray-800">
                    ¡Hola! 👋 Soy tu asistente inteligente para la gestión de cajones.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-2">
                <div className="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <svg className="w-3 h-3 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
                <div className="bg-white rounded-lg p-3 shadow-sm max-w-xs">
                  <p className="text-xs text-gray-800">
                    Puedo ayudarte con:
                  </p>
                  <ul className="text-xs text-gray-700 mt-1 space-y-1">
                    <li>• Organizar objetos</li>
                    <li>• Buscar objetos</li>
                    <li>• Optimizar espacio</li>
                    <li>• Sugerir ubicaciones</li>
                  </ul>
                </div>
              </div>

              <div className="flex items-start gap-2">
                <div className="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <svg className="w-3 h-3 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
                <div className="bg-white rounded-lg p-3 shadow-sm max-w-xs">
                  <p className="text-xs text-gray-800">
                    ¿En qué puedo ayudarte hoy? 🤔
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Input para escribir */}
          <div className="border-t border-gray-200 p-3 bg-white rounded-b-lg">
            <div className="flex gap-2">
              <input
                type="text"
                placeholder="Escribe aquí..."
                className="flex-1 px-2 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-transparent"
              />
              <button className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm transition-colors">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Botón flotante de chat */}
      <button
        onClick={toggleChat}
        className="bg-blue-600 hover:bg-blue-700 text-white p-4 rounded-full shadow-lg transition-all duration-300 hover:scale-110"
        title="Chat Inteligente"
      >
        {isOpen ? (
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        ) : (
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
        )}
      </button>
    </div>
  )
}

export default ChatInteligente
