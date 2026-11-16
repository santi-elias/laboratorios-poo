package com.gremio.controller;

import com.gremio.model.Contacto;
import com.gremio.service.ContactoService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;

@Controller
public class ContactoController {

    private final ContactoService service;

    // El controlador delega toda la lógica de negocio al Service (no habla directo con el Repository)
    public ContactoController(ContactoService service) {
        this.service = service;
    }

    // GET / → Redirige a la lista de contactos
    @GetMapping("/")
    public String inicio() {
        return "redirect:/contactos";
    }

    // GET /contactos → Muestra la lista de contactos
    @GetMapping("/contactos")
    public String listar(Model model) {
        model.addAttribute("contactos", service.listarTodos());
        return "contactos";
    }

    // GET /nuevo → Muestra el formulario vacío para crear un contacto
    @GetMapping("/nuevo")
    public String formularioNuevo(Model model) {
        model.addAttribute("contacto", new Contacto());
        return "formulario";
    }

    // POST /guardar → Recibe el formulario de nuevo contacto y lo guarda
    @PostMapping("/guardar")
    public String guardar(@ModelAttribute Contacto contacto) {
        service.guardar(contacto);
        return "redirect:/contactos";
    }

    // GET /editar/{id} → Carga el contacto por ID y abre el formulario pre-llenado
    @GetMapping("/editar/{id}")
    public String formularioEditar(@PathVariable Long id, Model model) {
        model.addAttribute("contacto", service.buscarPorId(id));
        return "formulario";
    }

    // POST /actualizar → Recibe el contacto editado (con ID) y guarda los cambios
    @PostMapping("/actualizar")
    public String actualizar(@ModelAttribute Contacto contacto) {
        service.guardar(contacto);
        return "redirect:/contactos";
    }

    // GET /eliminar/{id} → Elimina el contacto por ID y redirige a la lista
    @GetMapping("/eliminar/{id}")
    public String eliminar(@PathVariable Long id) {
        service.eliminar(id);
        return "redirect:/contactos";
    }
}
