package com.gremio.repository;

import com.gremio.model.Contacto;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ContactoRepository extends JpaRepository<Contacto, Long> {
    // Spring Data JPA genera dinámicamente en tiempo de ejecución las implementaciones para:
    // - save(entity): INSERT o UPDATE
    // - findAll(): SELECT * FROM contacto
    // - findById(id): SELECT * FROM contacto WHERE id = ?
    // - deleteById(id): DELETE FROM contacto WHERE id = ?
}
