package com.gremio;

import com.gremio.model.Contacto;
import com.gremio.repository.ContactoRepository;
import com.gremio.service.ContactoService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
class AgendaWebApplicationTests {

    @Autowired
    private ContactoService service;

    @Autowired
    private ContactoRepository repository;

    @Test
    void contextLoads() {
        assertNotNull(service, "El servicio de contactos debe inyectarse correctamente.");
        assertNotNull(repository, "El repositorio de contactos debe inyectarse correctamente.");
    }

    @Test
    void testFlujoCrudCompleto() {
        // 1. Create - Guardar contacto
        Contacto nuevo = new Contacto("Santiago", "Chaparro", "santiago.chaparro@uanl.edu.mx", "8110002222");
        service.guardar(nuevo);
        assertNotNull(nuevo.getId(), "El contacto guardado debe tener un ID asignado.");

        // 2. Read - Listar y buscar por ID
        List<Contacto> lista = service.listarTodos();
        assertFalse(lista.isEmpty(), "La lista de contactos no debe estar vacía.");

        Contacto encontrado = service.buscarPorId(nuevo.getId());
        assertEquals("Santiago", encontrado.getNombre());
        assertEquals("Chaparro", encontrado.getApellido());

        // 3. Update - Modificar contacto
        encontrado.setTelefono("8188889999");
        service.guardar(encontrado);
        Contacto actualizado = service.buscarPorId(nuevo.getId());
        assertEquals("8188889999", actualizado.getTelefono());

        // 4. Delete - Eliminar contacto
        Long idEliminar = actualizado.getId();
        service.eliminar(idEliminar);
        assertThrows(RuntimeException.class, () -> service.buscarPorId(idEliminar));
    }
}
