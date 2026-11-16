/**
 * Clase Druida - Personaje que domina las fuerzas de la naturaleza.
 * Puede lanzar hechizos (Hechicero) y curar aliados (Sanador).
 * Tiene una forma animal que potencia sus habilidades.
 */
public class Druida extends Personaje implements Hechicero, Sanador {

    private int mana;
    private int poderCuracion;
    private String formaAnimal; // forma bestial que puede adoptar

    public Druida(String nombre, int nivel, int puntosVida,
                  int mana, int poderCuracion, String formaAnimal) {
        super(nombre, nivel, puntosVida);
        this.mana = mana;
        this.poderCuracion = poderCuracion;
        this.formaAnimal = formaAnimal;
    }

    // --- Métodos abstractos de Personaje ---

    @Override
    public void atacar() {
        int danio = calcularDanio();
        System.out.println("[" + nombre + "] invoca raíces del bosque. Daño: " + danio);
    }

    @Override
    public int calcularDanio() {
        // Daño base por nivel + bonus de maná + bonus por forma animal
        int danioBase = nivel * 20;
        int bonusMana = mana / 2;
        int bonusForma = formaAnimal.equals("Oso") ? 40 : 20;
        return danioBase + bonusMana + bonusForma;
    }

    // --- Métodos de Hechicero ---

    @Override
    public void lanzarHechizo() {
        System.out.println(nombre + " lanza: ¡Tormenta de espinas! (maná: " + mana + ")");
    }

    @Override
    public int getMana() {
        return mana;
    }

    // --- Métodos de Sanador ---

    @Override
    public void curarAliado(Personaje aliado) {
        aliado.puntosVida += poderCuracion;
        System.out.println(nombre + " toca la tierra y cura a " + aliado.nombre +
                           " +" + poderCuracion + ". Vida: " + aliado.puntosVida);
    }

    @Override
    public int getPoderCuracion() {
        return poderCuracion;
    }

    // --- Getter propio ---

    public String getFormaAnimal() {
        return formaAnimal;
    }

    @Override
    public String toString() {
        return super.toString() + " | Forma Animal: " + formaAnimal;
    }
}
