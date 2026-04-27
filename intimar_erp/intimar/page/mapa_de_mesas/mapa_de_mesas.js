frappe.pages['mapa-de-mesas'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Mapa de Mesas Interactivo',
		single_column: true
	});

	page.set_primary_action('Refrescar', () => render_map(page), 'refresh');

	// Contenedor principal
	let container = $(`<div class="map-container" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 20px; padding: 20px;"></div>`).appendTo(page.body);

	function render_map(page) {
		container.empty();
		
		frappe.call({
			method: "frappe.client.get_list",
			args: {
				doctype: "Mesa Intimar",
				fields: ["name", "numero_mesa", "ubicacion_mesa", "estado_mesa"]
			},
			callback: function(r) {
				let mesas = r.message || [];
				
				mesas.forEach(mesa => {
					let status = mesa.estado_mesa ? "Disponible" : "Ocupada";
					let color = mesa.estado_mesa ? "#28a745" : "#dc3545"; 
					let info = mesa.ubicacion_mesa || "";

					let card = $(`
						<div class="mesa-card" style="border: 2px solid ${color}; border-radius: 8px; padding: 15px; text-align: center; cursor: pointer; transition: transform 0.2s;">
							<div style="font-size: 24px; font-weight: bold; color: ${color}; mb-10">Mesa ${mesa.numero_mesa}</div>
							<div style="font-size: 14px; color: #666;">${info}</div>
							<div style="margin-top: 10px; font-weight: bold; color: ${color}">${status}</div>
						</div>
					`).appendTo(container);

					card.hover(
						function() { $(this).css("transform", "scale(1.05)"); },
						function() { $(this).css("transform", "scale(1)"); }
					);

					card.click(() => {
						frappe.set_route("Form", "Mesa Intimar", mesa.name);
					});
				});
			}
		});
	}

	render_map(page);

	frappe.realtime.on("reserva_actualizada", function(data) {
		frappe.show_alert({message: `Reserva ${data.reserva} actualizada`, indicator: 'blue'});
		render_map(page);
	});
}
