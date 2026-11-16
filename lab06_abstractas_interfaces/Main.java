/**
 * Clase principal Main - Demuestra el uso de clases abstractas,
 * interfaces, polimorfismo e instanceof en la jerarquía del RPG.
 */
public class Main {

    public static void main(String[] args) {

        System.out.println("=== RPG — Expansión: Nuevas Clases ===\n");

        // -- Error esperado (línea comentada) --
        System.out.println("-- Error esperado (línea comentada) --");
        // new Personaje("X", 1, 100); // → cannot instantiate abstract class
        System.out.println("// new Personaje(...) → cannot instantiate abstract class\n");

        // Crear un objeto de cada tipo
        Druida druida = new Druida("Sylva", 7, 200, 180, 120, "Oso");
        Nigromante nigromante = new Nigromante("Malachar", 6, 350, 220, 5);
        Bardo bardo = new Bardo("Finnian", 5, 150, 60, "Laúd", 70);

        // -- Demostrar polimorfismo con arreglo Personaje[] --
        System.out.println("-- Ataques y daño --");
        Personaje[] equipo = { druida, nigromante, bardo };

        for (Personaje p : equipo) {
            p.atacar();
        }

        // -- Solo los Hechiceros lanzan hechizos --
        System.out.println("\n-- Solo los Hechiceros lanzan hechizos --");
        for (Personaje p : equipo) {
            if (p instanceof Hechicero h) {
                h.lanzarHechizo();
            }
        }

        // -- Solo los Sanadores curan --
        System.out.println("\n-- Solo los Sanadores curan --");
        nigromante.recibirDanio(300);

        // El Druida cura al Nigromante
        druida.curarAliado(nigromante);

        // El Bardo cura al Nigromante
        bardo.curarAliado(nigromante);

        // -- Estado final --
        System.out.println("\n-- Estado final --");
        for (Personaje p : equipo) {
            System.out.println(p);
        }
    }
}
