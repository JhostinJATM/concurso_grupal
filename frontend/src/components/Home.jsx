import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { dbUtils } from '../db/index.js'

const Home = () => {
  const navigate = useNavigate()
  const [cajones, setCajones] = useState([])
  const [objetos, setObjetos] = useState([])

  useEffect(() => {
    // Cargar todos los cajones y objetos de la base de datos
    const cajonesData = dbUtils.getAll('cajones')
    const objetosData = dbUtils.getAll('objetos')
    setCajones(cajonesData)
    setObjetos(objetosData)
  }, [])

  // Función para contar objetos por cajón
  const getObjetosCountByCajon = (cajonId) => {
    return objetos.filter(objeto => objeto.cajonId === cajonId).length
  }

  // Función para calcular porcentaje de ocupación
  const getOcupacionPorcentaje = (cajonId, capacidadMaxima) => {
    const objetosCount = getObjetosCountByCajon(cajonId)
    return Math.min((objetosCount / capacidadMaxima) * 100, 100)
  }

  const handleAgregarCajon = () => {
    // Funcionalidad pendiente
    console.log('Agregar cajón - Funcionalidad pendiente')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Sistema de Cajones
              </h1>
              <p className="mt-1 text-sm text-gray-500">
                Gestiona y organiza todos tus cajones
              </p>
            </div>
            <button
              onClick={handleAgregarCajon}
              className="bg-orange-600 hover:bg-orange-700 text-white px-6 py-3 rounded-lg text-sm font-medium flex items-center gap-2 shadow-sm transition-colors"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
              Agregar Cajón
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats */}
        <div className="mb-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Total de Cajones</p>
                  <p className="text-3xl font-bold text-gray-900">{cajones.length}</p>
                </div>
                <div className="bg-orange-100 p-3 rounded-full">
                  <svg className="w-8 h-8 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                  </svg>
                </div>
              </div>
            </div>
            
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Total de Objetos</p>
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
                  <p className="text-sm text-gray-500">Capacidad Total</p>
                  <p className="text-3xl font-bold text-gray-900">
                    {cajones.reduce((total, cajon) => total + cajon.capacidadMaxima, 0)}
                  </p>
                </div>
                <div className="bg-green-100 p-3 rounded-full">
                  <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Cajones Grid */}
        {cajones.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {cajones.map((cajon) => (
              <div
                key={cajon.id}
                className="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow duration-300 overflow-hidden border border-gray-100"
              >
                <div className="relative h-48 bg-gradient-to-br from-orange-100 to-orange-200">
                  <img
                    src="/assets/cajon.png"
                    alt={`Cajón ${cajon.nombre}`}
                    // className="w-full h-full"
                    className="h-full mx-auto"
                    onError={(e) => {
                      e.target.style.display = 'none'
                      e.target.nextSibling.style.display = 'flex'
                    }}
                  />
                  <div className="absolute inset-0 hidden items-center justify-center bg-gradient-to-br from-orange-100 to-orange-200">
                    <svg className="w-16 h-16 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                    </svg>
                  </div>
                  {/* Badge con ID */}
                  <div className="absolute top-3 left-3">
                    <span className="bg-white/90 backdrop-blur-sm text-gray-700 text-xs font-medium px-2 py-1 rounded-full">
                      #{cajon.id}
                    </span>
                  </div>
                </div>

                <div className="p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    {cajon.nombre}
                  </h3>
                  
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-500">Capacidad Máxima</span>
                      <span className="text-sm font-medium text-gray-900">
                        {cajon.capacidadMaxima} items
                      </span>
                    </div>

                    {/* Barra de progreso con datos reales */}
                    <div>
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm text-gray-500">Ocupación</span>
                        <span className="text-sm font-medium text-gray-900">
                          {getObjetosCountByCajon(cajon.id)} / {cajon.capacidadMaxima}
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className={`h-2 rounded-full ${
                            getOcupacionPorcentaje(cajon.id, cajon.capacidadMaxima) > 80 
                              ? 'bg-red-500' 
                              : getOcupacionPorcentaje(cajon.id, cajon.capacidadMaxima) > 60 
                              ? 'bg-yellow-500' 
                              : 'bg-green-500'
                          }`}
                          style={{width: `${getOcupacionPorcentaje(cajon.id, cajon.capacidadMaxima)}%`}}
                        ></div>
                      </div>
                    </div>
                  </div>

                  {/* Botones de acción */}
                  <div className="mt-6 flex gap-2">
                    <button 
                      onClick={() => navigate(`/gestion-cajon/${cajon.id}`)}
                      className="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 py-2 px-4 rounded-lg text-sm font-medium transition-colors"
                    >
                      Ver Detalles
                    </button>
                    <button 
                      onClick={() => navigate(`/gestion-cajon/${cajon.id}`)}
                      className="flex-1 bg-orange-600 hover:bg-orange-700 text-white py-2 px-4 rounded-lg text-sm font-medium transition-colors"
                    >
                      Gestionar
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          /* Estado vacío */
          <div className="text-center py-12">
            <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
            </svg>
            <h3 className="mt-2 text-sm font-medium text-gray-900">No hay cajones</h3>
            <p className="mt-1 text-sm text-gray-500">Comienza agregando tu primer cajón</p>
            <div className="mt-6">
              <button
                onClick={handleAgregarCajon}
                className="bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded-lg text-sm font-medium"
              >
                Agregar Cajón
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Home
