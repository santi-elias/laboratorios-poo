public class Main {

    public static void main(String[] args) {

        System.out.println("=== RPG — Sistema con Manejo de Excepciones ===");

        // Crear personajes para las pruebas
        Druida druida = new Druida("Sylva", 7, 200, 180, 120, "Oso");
        Nigromante nigromante = new Nigromante("Malachar", 6, 240, 220, 5);
        MotorCombate motor = new MotorCombate();

        // Escenario 1 — Turno normal sin excepción
        motor.ejecutarTurno(druida, nigromante);

        // Escenario 2 — Personaje derrotado intenta atacar
        try {
            druida.recibirDanio(9999); // primero derrota al druida
        } catch (AccionInvalidaException e) {
            System.out.println("Error al aplicar daño: " + e.getMessage());
        }
        motor.ejecutarTurno(druida, nigromante); // captura PersonajeDerrotadoException

        // Escenario 3 — Arquero sin flechas
        Arquero sinFlechas = new Arquero("Legolas", 6, 150, "Arco Largo", 0, 95);
        motor.ejecutarTurno(sinFlechas, nigromante); // captura RecursoInsuficienteException

        // Escenario 4 — Curar aliado derrotado
        System.out.println("\n-- Intento de curar aliado derrotado --");
        Druida druida2 = new Druida("Eldrin", 5, 180, 100, 80, "Lobo");
        try {
            druida2.curarAliado(druida); // druida está derrotado
        } catch (RpgException e) {
            System.out.println("No se pudo curar: " + e.getMessage());
        }

        // Escenario 5 — Daño negativo con finally
        System.out.println("\n-- Bloque manual try-catch-finally --");
        try {
            nigromante.recibirDanio(-50);
        } catch (AccionInvalidaException e) {
            System.out.println("Capturado: " + e.getMessage());
        } finally {
            System.out.println("El bloque finally siempre se ejecuta.");
        }

        // Escenario 6 — Mostrar bitácora completa
        motor.mostrarBitacora();
    }
}
