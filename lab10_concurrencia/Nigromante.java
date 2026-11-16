public class Nigromante extends Personaje implements Hechicero {

    private int mana;
    private int almasAbsorbidas;

    public Nigromante(String nombre, int nivel, int puntosVida, int mana) {
        this(nombre, nivel, puntosVida, mana, 5);
    }

    public Nigromante(String nombre, int nivel, int puntosVida,
                      int mana, int almasAbsorbidas) {
        super(nombre, nivel, puntosVida);
        this.mana = mana;
        this.almasAbsorbidas = almasAbsorbidas;
    }

    @Override
    public void atacar() throws RpgException {
        if (!isEstaVivo()) {
            throw new PersonajeDerrotadoException(getNombre());
        }

        if (mana < 15) {
            throw new RecursoInsuficienteException("mana", mana);
        }

        mana -= 15;
        System.out.println("[" + nombre + "] drena la esencia vital e invoca sombras.");
    }

    @Override
    public int calcularDanio() {
        int danioBase = nivel * 25;
        int bonusMana = mana / 2;
        int bonusAlmas = almasAbsorbidas * 15;
        return danioBase + bonusMana + bonusAlmas;
    }

    @Override
    public void lanzarHechizo() {
        System.out.println(nombre + " lanza: ¡Maldición de decadencia! (maná: " + mana + ")");
    }

    @Override
    public int getMana() {
        return mana;
    }

    public int getAlmasAbsorbidas() {
        return almasAbsorbidas;
    }

    @Override
    public String toString() {
        return super.toString() + " | Maná: " + mana + " | Almas: " + almasAbsorbidas;
    }
}
