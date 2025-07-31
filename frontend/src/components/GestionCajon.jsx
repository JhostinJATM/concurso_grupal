import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { dbUtils } from '../db/index.js'
import ChatInteligente from './ChatInteligente'

const GestionCajon = () => {
  const { cajonId } = useParams()
  const navigate = useNavigate()
  const [cajon, setCajon] = useState(null)
  const [objetos, setObjetos] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (cajonId) {
      // Cargar información del cajón
      const cajonData = dbUtils.getById('cajones', parseInt(cajonId))
      setCajon(cajonData)

      // Cargar objetos del cajón
      const objetosData = dbUtils.getObjetosByCajon(parseInt(cajonId))
      setObjetos(objetosData)
      
      setLoading(false)
    }
  }, [cajonId])

  const handleVolver = () => {
    navigate('/home')
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Cargando...</p>
        </div>
      </div>
    )
  }

  if (!cajon) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Cajón no encontrado</h2>
          <p className="text-gray-600 mb-4">El cajón que buscas no existe</p>
          <button
            onClick={handleVolver}
            className="bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded-lg"
          >
            Volver al inicio
          </button>
        </div>
      </div>
    )
  }

  const porcentajeOcupacion = Math.min((objetos.length / cajon.capacidadMaxima) * 100, 100)

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between py-6">
            <div className="flex items-center gap-4">
              <button
                onClick={handleVolver}
                className="text-gray-500 hover:text-gray-700 flex items-center gap-2"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
                Volver
              </button>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">
                  {cajon.nombre}
                </h1>
                <p className="mt-1 text-sm text-gray-500">
                  Gestión de objetos del cajón #{cajon.id}
                </p>
              </div>
            </div>
            <button className="bg-orange-600 hover:bg-orange-700 text-white px-6 py-3 rounded-lg text-sm font-medium flex items-center gap-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
              Agregar Objeto
            </button>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats del cajón */}
        <div className="mb-8 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500">Objetos en el cajón</p>
                <p className="text-3xl font-bold text-gray-900">{objetos.length}</p>
              </div>
              <div className="bg-blue-100 p-3 rounded-full">
                <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500">Capacidad máxima</p>
                <p className="text-3xl font-bold text-gray-900">{cajon.capacidadMaxima}</p>
              </div>
              <div className="bg-green-100 p-3 rounded-full">
                <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500">Ocupación</p>
                <p className="text-3xl font-bold text-gray-900">{Math.round(porcentajeOcupacion)}%</p>
              </div>
              <div className={`p-3 rounded-full ${
                porcentajeOcupacion > 80 ? 'bg-red-100' : 
                porcentajeOcupacion > 60 ? 'bg-yellow-100' : 'bg-green-100'
              }`}>
                <svg className={`w-8 h-8 ${
                  porcentajeOcupacion > 80 ? 'text-red-600' : 
                  porcentajeOcupacion > 60 ? 'text-yellow-600' : 'text-green-600'
                }`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
            </div>
          </div>
        </div>

        {/* Barra de progreso */}
        <div className="mb-8 bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-lg font-medium text-gray-900">Estado del cajón</h3>
            <span className="text-sm text-gray-500">{objetos.length} / {cajon.capacidadMaxima} objetos</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div 
              className={`h-3 rounded-full transition-all duration-300 ${
                porcentajeOcupacion > 80 ? 'bg-red-500' : 
                porcentajeOcupacion > 60 ? 'bg-yellow-500' : 'bg-green-500'
              }`}
              style={{width: `${porcentajeOcupacion}%`}}
            ></div>
          </div>
        </div>

        {/* Lista de objetos */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">Objetos en el cajón</h3>
          </div>
          
          {objetos.length > 0 ? (
            <div className="divide-y divide-gray-200">
              {objetos.map((objeto) => (
                <div key={objeto.id} className="px-6 py-4 hover:bg-gray-50">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <div className="flex-shrink-0">
                        <div className="w-10 h-10 bg-orange-100 rounded-full flex items-center justify-center">
                          <svg className="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                          </svg>
                        </div>
                      </div>
                      <div>
                        <h4 className="text-sm font-medium text-gray-900">{objeto.nombre}</h4>
                        <div className="flex items-center space-x-4 mt-1">
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                            {objeto.tipoObjeto}
                          </span>
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                            {objeto.tamanio}
                          </span>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <button className="text-indigo-600 hover:text-indigo-900 text-sm font-medium">
                        Editar
                      </button>
                      <button className="text-red-600 hover:text-red-900 text-sm font-medium">
                        Eliminar
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="px-6 py-12 text-center">
              <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
              <h3 className="mt-2 text-sm font-medium text-gray-900">No hay objetos</h3>
              <p className="mt-1 text-sm text-gray-500">Este cajón está vacío. Comienza agregando objetos.</p>
              <div className="mt-6">
                <button className="bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded-lg text-sm font-medium">
                  Agregar primer objeto
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Chat Inteligente */}
      <ChatInteligente />
    </div>
  )
}

export default GestionCajon
