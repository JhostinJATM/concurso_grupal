import React, { useState, useEffect } from "react";

/**
 * Componente para generar y mostrar recomendaciones inteligentes
 * Integra con el endpoint de recomendaciones del backend
 */
const RecomendacionesInteligentes = ({ userId, authToken }) => {
    const [recomendaciones, setRecomendaciones] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [generadoConIA, setGeneradoConIA] = useState(false);
    const [estadisticas, setEstadisticas] = useState(null);

    // Iconos para tipos de recomendaciones
    const tipoIconos = {
        ORGANIZACION: "📋",
        ESPACIO: "📦",
        MANTENIMIENTO: "🔧",
        SEGURIDAD: "🔒",
        EFICIENCIA: "⚡",
    };

    // Colores para prioridades
    const prioridadColores = {
        BAJA: "#28a745",
        MEDIA: "#ffc107",
        ALTA: "#fd7e14",
        CRITICA: "#dc3545",
    };

    /**
     * Generar recomendaciones automáticas
     */
    const generarRecomendaciones = async () => {
        setLoading(true);
        setError(null);

        try {
            const response = await fetch(
                "/api/cajones_inteligentes/recomendaciones/generar_automaticas/",
                {
                    method: "POST",
                    headers: {
                        Authorization: `Bearer ${authToken}`,
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        usuario_id: userId, // Opcional, usa el usuario autenticado si no se proporciona
                    }),
                }
            );

            const data = await response.json();

            if (response.ok) {
                setRecomendaciones(data.recomendaciones || []);
                setGeneradoConIA(data.generado_con_ia || false);
                setEstadisticas({
                    totalCajones: data.total_cajones,
                    totalObjetos: data.total_objetos,
                    totalRecomendaciones: data.total_recomendaciones_generadas,
                });
            } else {
                setError(data.error || "Error al generar recomendaciones");
            }
        } catch (err) {
            setError("Error de conexión. Verifica tu conexión a internet.");
            console.error("Error generando recomendaciones:", err);
        } finally {
            setLoading(false);
        }
    };

    /**
     * Cargar recomendaciones existentes
     */
    const cargarRecomendacionesExistentes = async () => {
        try {
            const response = await fetch(
                "/api/cajones_inteligentes/recomendaciones/",
                {
                    headers: {
                        Authorization: `Bearer ${authToken}`,
                    },
                }
            );

            if (response.ok) {
                const data = await response.json();
                setRecomendaciones(data.results || []);
            }
        } catch (err) {
            console.error("Error cargando recomendaciones:", err);
        }
    };

    /**
     * Marcar recomendación como implementada
     */
    const marcarImplementada = async (recomendacionId) => {
        try {
            const response = await fetch(
                `/api/cajones_inteligentes/recomendaciones/${recomendacionId}/marcar_implementada/`,
                {
                    method: "POST",
                    headers: {
                        Authorization: `Bearer ${authToken}`,
                        "Content-Type": "application/json",
                    },
                }
            );

            if (response.ok) {
                // Actualizar la recomendación en el estado local
                setRecomendaciones((prev) =>
                    prev.map((rec) =>
                        rec.id === recomendacionId
                            ? { ...rec, implementada: true }
                            : rec
                    )
                );
            }
        } catch (err) {
            console.error("Error marcando recomendación:", err);
        }
    };

    // Cargar recomendaciones existentes al montar el componente
    useEffect(() => {
        if (authToken) {
            cargarRecomendacionesExistentes();
        }
    }, [authToken]);

    return (
        <div className="recomendaciones-container">
            <div className="recomendaciones-header">
                <h2>🤖 Recomendaciones Inteligentes</h2>
                <p>
                    Analiza tus cajones y obtén sugerencias personalizadas para
                    optimizar tu organización
                </p>

                <button
                    onClick={generarRecomendaciones}
                    disabled={loading}
                    className="btn-generar-recomendaciones"
                >
                    {loading
                        ? "🔄 Generando..."
                        : "✨ Generar Nuevas Recomendaciones"}
                </button>
            </div>

            {/* Estadísticas */}
            {estadisticas && (
                <div className="estadisticas-panel">
                    <h3>📊 Análisis de tu Organización</h3>
                    <div className="stats-grid">
                        <div className="stat-item">
                            <span className="stat-number">
                                {estadisticas.totalCajones}
                            </span>
                            <span className="stat-label">Cajones</span>
                        </div>
                        <div className="stat-item">
                            <span className="stat-number">
                                {estadisticas.totalObjetos}
                            </span>
                            <span className="stat-label">Objetos</span>
                        </div>
                        <div className="stat-item">
                            <span className="stat-number">
                                {estadisticas.totalRecomendaciones}
                            </span>
                            <span className="stat-label">Recomendaciones</span>
                        </div>
                    </div>
                    <div className="ia-badge">
                        {generadoConIA
                            ? "🤖 Generado con IA"
                            : "📋 Análisis básico"}
                    </div>
                </div>
            )}

            {/* Error */}
            {error && <div className="error-message">❌ {error}</div>}

            {/* Lista de Recomendaciones */}
            <div className="recomendaciones-lista">
                {recomendaciones.length === 0 && !loading ? (
                    <div className="no-recomendaciones">
                        <p>💡 No hay recomendaciones disponibles</p>
                        <p>
                            Haz clic en "Generar Nuevas Recomendaciones" para
                            obtener sugerencias personalizadas
                        </p>
                    </div>
                ) : (
                    recomendaciones.map((rec, index) => (
                        <RecomendacionCard
                            key={rec.id || index}
                            recomendacion={rec}
                            tipoIconos={tipoIconos}
                            prioridadColores={prioridadColores}
                            onMarcarImplementada={() =>
                                marcarImplementada(rec.id)
                            }
                        />
                    ))
                )}
            </div>
        </div>
    );
};

/**
 * Componente para mostrar una recomendación individual
 */
const RecomendacionCard = ({
    recomendacion,
    tipoIconos,
    prioridadColores,
    onMarcarImplementada,
}) => {
    const icono =
        tipoIconos[recomendacion.tipo_recomendacion || recomendacion.tipo] ||
        "💡";
    const color = prioridadColores[recomendacion.prioridad] || "#6c757d";

    return (
        <div
            className={`recomendacion-card ${
                recomendacion.implementada ? "implementada" : ""
            }`}
        >
            <div className="recomendacion-header">
                <div className="tipo-icono">{icono}</div>
                <h4 className="recomendacion-titulo">
                    {recomendacion.nombre || recomendacion.titulo}
                </h4>
                <div
                    className="prioridad-badge"
                    style={{ backgroundColor: color }}
                >
                    {recomendacion.prioridad}
                </div>
            </div>

            <p className="recomendacion-descripcion">
                {recomendacion.descripcion}
            </p>

            {recomendacion.razon && (
                <div className="recomendacion-razon">
                    <strong>💡 ¿Por qué es importante?</strong>
                    <p>{recomendacion.razon}</p>
                </div>
            )}

            <div className="recomendacion-footer">
                <span className="tipo-label">
                    {recomendacion.tipo_recomendacion || recomendacion.tipo}
                </span>

                {!recomendacion.implementada && (
                    <button
                        onClick={onMarcarImplementada}
                        className="btn-implementar"
                    >
                        ✅ Marcar como Implementada
                    </button>
                )}

                {recomendacion.implementada && (
                    <span className="implementada-badge">✅ Implementada</span>
                )}
            </div>

            {recomendacion.fecha_creacion && (
                <div className="fecha-creacion">
                    📅{" "}
                    {new Date(
                        recomendacion.fecha_creacion
                    ).toLocaleDateString()}
                </div>
            )}
        </div>
    );
};

export default RecomendacionesInteligentes;

/* CSS Sugerido */
const estilosCSS = `
.recomendaciones-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.recomendaciones-header {
  text-align: center;
  margin-bottom: 30px;
}

.btn-generar-recomendaciones {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: transform 0.2s;
}

.btn-generar-recomendaciones:hover {
  transform: translateY(-2px);
}

.btn-generar-recomendaciones:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.estadisticas-panel {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 30px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 20px;
  margin: 20px 0;
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 2em;
  font-weight: bold;
  color: #667eea;
}

.stat-label {
  display: block;
  color: #6c757d;
  margin-top: 5px;
}

.ia-badge {
  text-align: center;
  background: #e3f2fd;
  color: #1976d2;
  padding: 8px 16px;
  border-radius: 20px;
  display: inline-block;
  font-size: 14px;
  font-weight: 500;
}

.error-message {
  background: #f8d7da;
  color: #721c24;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  border: 1px solid #f5c6cb;
}

.no-recomendaciones {
  text-align: center;
  padding: 40px;
  color: #6c757d;
}

.recomendacion-card {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.recomendacion-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.recomendacion-card.implementada {
  opacity: 0.7;
  background: #f8f9fa;
}

.recomendacion-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 15px;
}

.tipo-icono {
  font-size: 24px;
}

.recomendacion-titulo {
  flex: 1;
  margin: 0;
  color: #333;
}

.prioridad-badge {
  color: white;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: bold;
  text-transform: uppercase;
}

.recomendacion-descripcion {
  color: #555;
  line-height: 1.6;
  margin-bottom: 15px;
}

.recomendacion-razon {
  background: #f8f9fa;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 15px;
  border-left: 4px solid #667eea;
}

.recomendacion-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tipo-label {
  background: #e9ecef;
  color: #495057;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  text-transform: uppercase;
}

.btn-implementar {
  background: #28a745;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}

.implementada-badge {
  color: #28a745;
  font-weight: 500;
}

.fecha-creacion {
  font-size: 12px;
  color: #6c757d;
  margin-top: 10px;
  text-align: right;
}
`;

export { estilosCSS };
