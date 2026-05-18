export function generateReservasPDF(allReservas, activeFilters, visibleColumns) {
  const { jsPDF } = window.jspdf
  const doc = new jsPDF()
  
  // Estética del Header con el celeste de la marca (#00938F)
  doc.setFillColor(0, 147, 143) // RGB del #00938F
  doc.rect(0, 0, 210, 45, 'F')
  
  doc.setTextColor(255, 255, 255)
  doc.setFontSize(24)
  doc.setFont('helvetica', 'bold')
  doc.text('INTIMAR', 14, 22)
  doc.setFontSize(14)
  doc.text('LISTADO DE RESERVAS', 14, 32)
  
  doc.setFontSize(9)
  doc.setFont('helvetica', 'normal')
  doc.text(`Generado el: ${new Date().toLocaleString()}`, 14, 40)
  
  // Filtros aplicados
  let filterText = "Reporte de disponibilidad basado en filtros actuales"
  if (activeFilters.fecha) {
    const parts = activeFilters.fecha.split('-')
    const formattedFilterDate = parts.length === 3 ? `${parts[2]}-${parts[1]}-${parts[0]}` : activeFilters.fecha
    filterText = `Reservas para el día: ${formattedFilterDate}`
  }
  
  doc.setTextColor(80, 80, 80)
  doc.setFontSize(9)
  doc.setFont('helvetica', 'bolditalic')
  doc.text(filterText, 14, 55)

  // Construir columnas dinámicamente según visibleColumns
  const columns = []
  
  // Siempre incluimos ID Reserva como columna base
  columns.push({ header: 'ID', dataKey: 'nro' })
  
  if (visibleColumns.motivo) {
    columns.push({ header: 'ORIGEN', dataKey: 'motivo' })
  }
  
  if (visibleColumns.cliente) {
    columns.push({ header: 'CLIENTE', dataKey: 'cliente' })
  }
  
  if (visibleColumns.detalles) {
    // Si hay filtro de fecha activo, omitimos FECHA en cada fila ya que es redundante y se muestra en el subtítulo
    if (!activeFilters.fecha) {
      columns.push({ header: 'FECHA', dataKey: 'fecha' })
    }
    columns.push({ header: 'HORA', dataKey: 'hora' })
    columns.push({ header: 'PERS.', dataKey: 'personas' })
  }
  
  if (visibleColumns.llegada) {
    columns.push({ header: 'LLEGADA', dataKey: 'llegada' })
  }
  
  if (visibleColumns.salida) {
    columns.push({ header: 'SALIDA', dataKey: 'salida' })
  }
  
  if (visibleColumns.pago) {
    columns.push({ header: 'MEDIO', dataKey: 'pagoMedio' })
    columns.push({ header: 'ANTICIPO', dataKey: 'pagoMonto' })
    columns.push({ header: 'OPERACIÓN', dataKey: 'pagoOp' })
  }
  
  if (visibleColumns.mesas) {
    columns.push({ header: 'MESA', dataKey: 'mesa' })
    columns.push({ header: 'MOZO', dataKey: 'mozo' })
  }
  
  if (visibleColumns.creacion) {
    columns.push({ header: 'CREACIÓN', dataKey: 'creacion' })
  }

  const rows = allReservas.map(res => {
    // Formatear fecha de YYYY-MM-DD a DD-MM-YYYY
    const dateParts = res.fecha_reserva?.split('-') || []
    const formattedDate = dateParts.length === 3 ? `${dateParts[2]}-${dateParts[1]}-${dateParts[0]}` : res.fecha_reserva

    // Formatear creación
    let creationStr = '---'
    if (res.creation) {
      const parts = res.creation.split(' ')
      if (parts.length > 0) {
        const cParts = parts[0].split('-')
        creationStr = cParts.length === 3 ? `${cParts[2]}-${cParts[1]}-${cParts[0]}` : parts[0]
      }
    }

    // Nombre de cliente
    const clienteName = `${res.nombre} ${res.apellido || ''}`.trim().toUpperCase()

    // Formatear mesas asignadas
    let mesaStr = '---'
    if (res.mesas?.length) {
      mesaStr = res.mesas.map(m => m.mesa).join(', ')
    }

    let medioStr = '---'
    let montoStr = '---'
    let opStr = '---'

    if (res.anticipos?.length) {
      medioStr = res.anticipos.map(a => (a.banco || 'PAGO').toUpperCase()).join('\n')
      montoStr = res.anticipos.map(a => `${a.moneda} ${parseFloat(a.monto_anticipo).toFixed(2)}`).join('\n')
      opStr = res.anticipos.map(a => a.nro_operacion || '---').join('\n')
    } else if (res.anticipo_required) {
      montoStr = 'SIN REGISTRAR'
    } else {
      montoStr = 'NO REQUIERE'
    }

    // Formatear motivo para el PDF
    const motivoStr = res.motivo_reserva ? res.motivo_reserva.replace(/[\[\]]/g, '').trim().toUpperCase() : 'INTERNA'

    return {
      nro: res.name,
      cliente: clienteName,
      personas: `${(res.cant_adultos || 0) + (res.cant_ninos || 0)}`,
      fecha: formattedDate,
      hora: `${res.hora_reserva ? res.hora_reserva.substring(0, 5) : ''}`,
      llegada: res.hora_llegada ? res.hora_llegada.substring(0, 5) : '---',
      salida: res.hora_salida ? res.hora_salida.substring(0, 5) : '---',
      pagoMedio: medioStr,
      pagoMonto: montoStr,
      pagoOp: opStr,
      mesa: mesaStr,
      mozo: res.mozo || '---',
      creacion: creationStr,
      motivo: motivoStr
    }
  })

  // Calcular tamaño de fuente dinámico según el número de columnas para evitar encogimiento o desborde
  const activeColCount = columns.length
  let fontSize = 8.5
  let cellPadding = 2.5
  if (activeColCount > 7) {
    fontSize = 6.5
    cellPadding = 1.8
  } else if (activeColCount > 5) {
    fontSize = 7.5
    cellPadding = 2.2
  }

  doc.autoTable({
    columns: columns,
    body: rows,
    startY: 60,
    margin: { left: 10, right: 10 },
    styles: { 
      fontSize: fontSize, 
      cellPadding: cellPadding,
      font: 'helvetica',
      valign: 'middle'
    },
    headStyles: { 
      fillColor: [0, 147, 143], 
      textColor: [255, 255, 255],
      fontStyle: 'bold',
      halign: 'center',
      fontSize: fontSize + 0.5
    },
    alternateRowStyles: {
      fillColor: [245, 252, 252]
    }
  })

  // Obtener la posición final y agregar los totales basados en todo el universo filtrado
  const finalY = doc.lastAutoTable.finalY || 80
  const totalPax = allReservas.reduce((acc, res) => acc + (res.cant_adultos || 0) + (res.cant_ninos || 0), 0)
  const totalReservas = allReservas.length
  
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(10)
  doc.setTextColor(0, 147, 143) // Color de marca #00938F
  doc.text(`TOTAL DE PERSONAS: ${totalPax}`, 14, finalY + 12)
  doc.text(`TOTAL DE RESERVAS: ${totalReservas}`, 14, finalY + 18)

  doc.save(`reservas_intimar_${new Date().toISOString().split('T')[0]}.pdf`)
}
