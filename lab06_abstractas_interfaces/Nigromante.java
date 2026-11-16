/**
 * Clase Nigromante - Personaje que manipula la energía oscura.
 * Puede lanzar hechizos (Hechicero) pero NO puede curar.
 * Absorbe almas de sus enemigos para volverse más poderoso.
 */
public class Nigromante extends Personaje implements Hechicero {

    private int mana;
    private int almasAbsorbidas; // cada alma incrementa su poder

    public Nigromante(String nombre, int nivel, int puntosVida,
                      int mana, int almasAbsorbidas) {
        super(nombre, nivel, puntosVida);
        this.mana = mana;
        this.almasAbsorbidas = almasAbsorbidas;
    }

    // --- Métodos abstractos de Personaje ---

    @Override
    public void atacar() {
        int danio = calcularDanio();
        System.out.println("[" + nombre + "] drena la esencia vital. Daño: " + danio);
    }

    @Override
    public int calcularDanio() {
        // Daño base por nivel + bonus de maná + bonus por almas absorbidas
        int danioBase = nivel * 25;
        int bonusMana = mana / 2;
        int bonusAlmas = almasAbsorbidas * 15;
        return danioBase + bonusMana + bonusAlmas;
    }

    // --- Métodos de Hechicero ---

    @Override
    public void lanzarHechizo() {
        System.out.println(nombre + " lanza: ¡Maldición de decadencia! (maná: " + mana + ")");
    }

    @Override
    public int getMana() {
        return mana;
    }

    // --- Getters propios ---

    public int getAlmasAbsorbidas() {
        return almasAbsorbidas;
    }

    @Override
    public String toString() {
        return super.toString() + " | Almas: " + almasAbsorbidas;
    }
}
