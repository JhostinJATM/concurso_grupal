import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { toast } from 'react-toastify'
import { cajonService } from '../services/cajonService'
import { objetoService } from '../services/objetoService'
import FormularioObjeto from './FormularioObjeto'
import Modal from './Modal'
import ChatInteligente from './ChatInteligente'

const GestionCajon = () => {
  const { cajonId } = useParams()
  const navigate = useNavigate()
  const [cajon, setCajon] = useState(null)
  const [objetos, setObjetos] = useState([])
  const [loading, setLoading] = useState(true)
  const [modalObjeto, setModalObjeto] = useState(false)
  const [objetoSeleccionado, setObjetoSeleccionado] = useState(null)

  const cargarDatos = async () => {
    setLoading(true)
    try {
      const [cajonData, objetosData] = await Promise.all([
        cajonService.getCajon(cajonId),
        objetoService.getObjetosByCajon(cajonId)
      ])
      
      setCajon(cajonData)
      setObjetos(objetosData.results || objetosData)
    } catch (error) {
      console.error('Error cargando datos:', error)
      toast.error('Error al cargar los datos del cajón')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (cajonId) {
      cargarDatos()
    }
  }, [cajonId])

  const handleVolver = () => {
    navigate('/home')
  }

  const handleAgregarObjeto = () => {
    setObjetoSeleccionado(null)
    setModalObjeto(true)
  }

  const handleEditarObjeto = (objeto) => {
    setObjetoSeleccionado(objeto)
    setModalObjeto(true)
  }

  const handleEliminarObjeto = async (objeto) => {
    if (window.confirm(`¿Estás seguro de que quieres eliminar el objeto "${objeto.nombre}"?`)) {
      try {
        await objetoService.deleteObjeto(objeto.id)
        toast.success('Objeto eliminado exitosamente')
        cargarDatos()
      } catch (error) {
        toast.error(error.message || 'Error al eliminar el objeto')
      }
    }
  }

  const handleSuccessObjeto = () => {
    setModalObjeto(false)
    setObjetoSeleccionado(null)
    cargarDatos()
  }

  const getTipoColor = (tipo) => {
    const colores = {
      'ROPA': 'bg-pink-100 text-pink-800',
      'PAPELERIA': 'bg-blue-100 text-blue-800',
      'CABLES': 'bg-gray-100 text-gray-800',
      'ELECTRONICA': 'bg-green-100 text-green-800',
      'LIBROS': 'bg-yellow-100 text-yellow-800',
      'HERRAMIENTAS': 'bg-red-100 text-red-800',
      'COCINA': 'bg-orange-100 text-orange-800',
      'OTROS': 'bg-purple-100 text-purple-800'
    }
    return colores[tipo] || 'bg-gray-100 text-gray-800'
  }

  const getTamanioIcon = (tamanio) => {
    switch (tamanio) {
      case 'PEQUENO':
        return <div className="w-3 h-3 bg-green-500 rounded-full"></div>
      case 'MEDIANO':
        return <div className="w-4 h-4 bg-yellow-500 rounded-full"></div>
      case 'GRANDE':
        return <div className="w-5 h-5 bg-red-500 rounded-full"></div>
      default:
        return <div className="w-4 h-4 bg-gray-500 rounded-full"></div>
    }
  }

  const getTamanioLabel = (tamanio) => {
    const labels = {
      'PEQUENO': 'Pequeño',
      'MEDIANO': 'Mediano',
      'GRANDE': 'Grande'
    }
    return labels[tamanio] || tamanio
  }

  const getTipoLabel = (tipo) => {
    const labels = {
      'ROPA': 'Ropa',
      'PAPELERIA': 'Papelería',
      'CABLES': 'Cables',
      'ELECTRONICA': 'Electrónica',
      'LIBROS': 'Libros',
      'HERRAMIENTAS': 'Herramientas',
      'COCINA': 'Artículos de Cocina',
      'OTROS': 'Otros'
    }
    return labels[tipo] || tipo
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

  const porcentajeOcupacion = Math.min((objetos.length / cajon.capacidad_maxima) * 100, 100)

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
            <button 
              onClick={handleAgregarObjeto}
              className="bg-orange-600 hover:bg-orange-700 text-white px-6 py-3 rounded-lg text-sm font-medium flex items-center gap-2"
            >
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
                <p className="text-3xl font-bold text-gray-900">{cajon.capacidad_maxima}</p>
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
            <span className="text-sm text-gray-500">{objetos.length} / {cajon.capacidad_maxima} objetos</span>
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

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Lista de objetos */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow">
              <div className="px-6 py-4 border-b border-gray-200">
                <h2 className="text-lg font-medium text-gray-900">Objetos en el cajón</h2>
              </div>
              
              {objetos.length > 0 ? (
                <div className="divide-y divide-gray-200">
                  {objetos.map((objeto) => (
                    <div key={objeto.id} className="p-6 hover:bg-gray-50">
                      <div className="flex items-center justify-between">
                        <div className="flex-1">
                          <div className="flex items-center gap-3 mb-2">
                            <h3 className="text-lg font-medium text-gray-900">{objeto.nombre}</h3>
                            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getTipoColor(objeto.tipo_objeto)}`}>
                              {getTipoLabel(objeto.tipo_objeto)}
                            </span>
                          </div>
                          
                          <div className="flex items-center gap-4 text-sm text-gray-500">
                            <div className="flex items-center gap-1">
                              {getTamanioIcon(objeto.tamanio)}
                              <span>{getTamanioLabel(objeto.tamanio)}</span>
                            </div>
                            <span>Agregado: {new Date(objeto.fecha_ingreso).toLocaleDateString()}</span>
                          </div>
                          
                          {objeto.descripcion && (
                            <p className="mt-2 text-sm text-gray-600">{objeto.descripcion}</p>
                          )}
                        </div>
                        
                        <div className="flex items-center gap-2 ml-4">
                          <button
                            onClick={() => handleEditarObjeto(objeto)}
                            className="text-blue-600 hover:text-blue-700 p-2 rounded-lg hover:bg-blue-50"
                          >
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                            </svg>
                          </button>
                          <button
                            onClick={() => handleEliminarObjeto(objeto)}
                            className="text-red-600 hover:text-red-700 p-2 rounded-lg hover:bg-red-50"
                          >
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                            </svg>
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-12">
                  <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                  </svg>
                  <h3 className="mt-2 text-lg font-medium text-gray-900">No hay objetos</h3>
                  <p className="mt-1 text-gray-500">Este cajón está vacío. Agrega tu primer objeto.</p>
                  <button
                    onClick={handleAgregarObjeto}
                    className="mt-4 bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded-lg text-sm font-medium flex items-center gap-2 mx-auto"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                    </svg>
                    Agregar Objeto
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* Chat inteligente */}
          <div className="lg:col-span-1">
            <ChatInteligente />
          </div>
        </div>
      </div>

      {/* Modal para objetos */}
      <Modal isOpen={modalObjeto} onClose={() => setModalObjeto(false)} size="md">
        <FormularioObjeto 
          objeto={objetoSeleccionado}
          cajonPredeterminado={cajon}
          onSuccess={handleSuccessObjeto}
          onCancel={() => setModalObjeto(false)}
        />
      </Modal>
    </div>
  )
}

export default GestionCajon
