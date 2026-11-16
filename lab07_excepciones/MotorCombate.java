import java.util.ArrayList;

public class MotorCombate {

    private ArrayList<String> bitacora;

    public MotorCombate() {
        bitacora = new ArrayList<>();
    }

    public void ejecutarTurno(Personaje atacante, Personaje defensor) {

        if (atacante == null) throw new PersonajeNuloException("ejecutarTurno(atacante)");
        if (defensor == null) throw new PersonajeNuloException("ejecutarTurno(defensor)");

        System.out.println("\n--- Turno: " + atacante.getNombre() +
                           " vs " + defensor.getNombre() + " ---");
        try {
            atacante.atacar();
            int danio = atacante.calcularDanio();
            defensor.recibirDanio(danio);
            bitacora.add(String.format("%-12s | %s atacó a %s (daño: %d)",
                         "OK", atacante.getNombre(), defensor.getNombre(), danio));

        } catch (PersonajeDerrotadoException e) {
            bitacora.add(String.format("%-12s | %s no pudo actuar",
                         "DERROTA", e.getNombrePersonaje()));
            System.out.println("⚠ " + e.getMessage());

        } catch (RecursoInsuficienteException e) {
            bitacora.add(String.format("%-12s | %s no pudo atacar",
                         "SIN RECURSO", atacante.getNombre()));
            System.out.println("⚠ " + e.getMessage());

        } catch (RpgException e) {
            bitacora.add(String.format("%-12s | %s",
                         "ERROR RPG", e.getMessage()));
            System.out.println("⚠ Error de juego: " + e.getMessage());

        } finally {
            // Siempre se ejecuta, haya o no excepción
            System.out.println("[Bitácora] Turno registrado.");
        }
    }

    public void mostrarBitacora() {
        System.out.println("\n=== Bitácora de Combate ===");
        for (int i = 0; i < bitacora.size(); i++) {
            System.out.println((i + 1) + ". " + bitacora.get(i));
        }
    }
}
