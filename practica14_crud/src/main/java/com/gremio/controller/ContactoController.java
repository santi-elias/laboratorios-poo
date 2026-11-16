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

    public ContactoController(ContactoService service) {
        this.service = service;
    }

    // Redirigir la raíz a /contactos
    @GetMapping("/")
    public String inicio() {
        return "redirect:/contactos";
    }

    // Listar todos los contactos
    @GetMapping("/contactos")
    public String listarContactos(Model model) {
        model.addAttribute("contactos", service.listarTodos());
        return "contactos";
    }

    // Mostrar formulario para nuevo contacto
    @GetMapping("/nuevo")
    public String formularioNuevo(Model model) {
        model.addAttribute("contacto", new Contacto());
        return "formulario";
    }

    // Guardar nuevo contacto
    @PostMapping("/guardar")
    public String guardar(@ModelAttribute Contacto contacto) {
        service.guardar(contacto);
        return "redirect:/contactos";
    }

    // Mostrar formulario para editar contacto existente
    @GetMapping("/editar/{id}")
    public String formularioEditar(@PathVariable Long id, Model model) {
        Contacto contacto = service.buscarPorId(id);
        model.addAttribute("contacto", contacto);
        return "formulario";
    }

    // Actualizar contacto existente
    @PostMapping("/actualizar")
    public String actualizar(@ModelAttribute Contacto contacto) {
        service.guardar(contacto);
        return "redirect:/contactos";
    }

    // Eliminar contacto por ID
    @GetMapping("/eliminar/{id}")
    public String eliminar(@PathVariable Long id) {
        service.eliminar(id);
        return "redirect:/contactos";
    }
}
