package com.gremio.repository;

import com.gremio.model.Contacto;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ContactoRepository extends JpaRepository<Contacto, Long> {
    // Spring Data JPA provee automáticamente:
    // save(), findAll(), findById(), deleteById(), etc.
}
