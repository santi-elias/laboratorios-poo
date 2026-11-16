package com.gremio.controller;

import com.gremio.model.Contacto;
import com.gremio.repository.ContactoRepository;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;

import java.util.Optional;

@Controller
public class ContactoController {

    private final ContactoRepository repo;

    // Inyección de dependencias por constructor (buena práctica recomendada por Spring)
    public ContactoController(ContactoRepository repo) {
        this.repo = repo;
    }

    // GET / → Redirige automáticamente al listado de contactos
    @GetMapping("/")
    public String inicio() {
        return "redirect:/contactos";
    }

    // GET /contactos → Muestra la lista de todos los contactos almacenados en BD
    @GetMapping("/contactos")
    public String listar(Model model) {
        model.addAttribute("contactos", repo.findAll());
        return "contactos";
    }

    // GET /nuevo → Muestra el formulario para capturar un nuevo contacto
    @GetMapping("/nuevo")
    public String formularioNuevo(Model model) {
        model.addAttribute("contacto", new Contacto());
        return "nuevo";
    }

    // POST /guardar → Procesa el formulario y guarda en la BD (INSERT o UPDATE según si tiene ID)
    @PostMapping("/guardar")
    public String guardar(@ModelAttribute Contacto contacto) {
        repo.save(contacto);
        return "redirect:/contactos";
    }

    // =========================================================================
    // MÓDULOS DE UPDATE Y DELETE (Requerimiento del laboratorio)
    // =========================================================================

    // GET /editar/{id} → Carga el contacto por ID y abre el formulario de edición
    @GetMapping("/editar/{id}")
    public String formularioEditar(@PathVariable("id") Long id, Model model) {
        Optional<Contacto> contactoOpt = repo.findById(id);
        if (contactoOpt.isPresent()) {
            model.addAttribute("contacto", contactoOpt.get());
            return "editar";
        }
        return "redirect:/contactos";
    }

    // GET /eliminar/{id} → Elimina el contacto de la BD por su ID y redirige a la lista
    @GetMapping("/eliminar/{id}")
    public String eliminar(@PathVariable("id") Long id) {
        if (repo.existsById(id)) {
            repo.deleteById(id);
        }
        return "redirect:/contactos";
    }

    // POST /eliminar/{id} → Soporte alternativo mediante POST para clientes que prefieran verbo POST
    @PostMapping("/eliminar/{id}")
    public String eliminarPost(@PathVariable("id") Long id) {
        if (repo.existsById(id)) {
            repo.deleteById(id);
        }
        return "redirect:/contactos";
    }
}
